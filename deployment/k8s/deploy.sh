#!/bin/bash
# Kubernetes deployment script for Vedic Astrology Calculator

set -e

NAMESPACE="vedic-astrology"
APP_NAME="vedic-astrology-calculator"
DOMAIN="${1:-vedic-astrology.your-domain.com}"

echo "🚀 Deploying Vedic Astrology Calculator to Kubernetes"
echo "Namespace: $NAMESPACE"
echo "Domain: $DOMAIN"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if we can connect to the cluster
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

# Create namespace
echo "📦 Creating namespace..."
kubectl apply -f namespace.yaml

# Wait for namespace to be ready
kubectl wait --for=condition=ready namespace/$NAMESPACE --timeout=60s

# Create secrets (you should customize this with actual secret values)
echo "🔐 Creating secrets..."
kubectl create secret generic vedic-astrology-secrets \
    --from-literal=SECRET_KEY="$(openssl rand -base64 32)" \
    --from-literal=API_KEY_ENFORCEMENT_ENABLED="true" \
    --namespace=$NAMESPACE \
    --dry-run=client -o yaml | kubectl apply -f -

# Create ephemeris data configmap
echo "📊 Creating ephemeris data configmap..."
if [ -d "../../ephe" ]; then
    kubectl create configmap ephemeris-data \
        --from-file=../../ephe \
        --namespace=$NAMESPACE \
        --dry-run=client -o yaml | kubectl apply -f -
else
    echo "⚠️  Ephemeris data directory not found. Creating empty configmap."
    kubectl create configmap ephemeris-data \
        --from-literal=placeholder="ephemeris data goes here" \
        --namespace=$NAMESPACE \
        --dry-run=client -o yaml | kubectl apply -f -
fi

# Apply configuration
echo "⚙️  Applying configuration..."
kubectl apply -f configmap.yaml

# Create persistent volume claim
echo "💾 Creating persistent storage..."
kubectl apply -f pvc.yaml

# Deploy the application
echo "🚀 Deploying application..."
kubectl apply -f deployment.yaml

# Create services
echo "🌐 Creating services..."
kubectl apply -f service.yaml

# Update ingress with correct domain
echo "🔗 Configuring ingress..."
sed "s/vedic-astrology.your-domain.com/$DOMAIN/g" ingress.yaml | kubectl apply -f -

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available deployment/vedic-astrology-app --namespace=$NAMESPACE --timeout=300s

# Check if pods are running
echo "🔍 Checking pod status..."
kubectl get pods -n $NAMESPACE

# Show services
echo "🌐 Services:"
kubectl get services -n $NAMESPACE

# Show ingress
echo "🔗 Ingress:"
kubectl get ingress -n $NAMESPACE

# Get external IP
EXTERNAL_IP=$(kubectl get service vedic-astrology-nodeport -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")

if [ "$EXTERNAL_IP" != "pending" ] && [ -n "$EXTERNAL_IP" ]; then
    echo "✅ Deployment complete!"
    echo "🌐 Application URL: http://$EXTERNAL_IP"
    echo "🌐 Domain URL: https://$DOMAIN"
else
    # Get NodePort for testing
    NODE_PORT=$(kubectl get service vedic-astrology-nodeport -n $NAMESPACE -o jsonpath='{.spec.ports[0].nodePort}')
    echo "✅ Deployment complete!"
    echo "🌐 NodePort URL: http://<node-ip>:$NODE_PORT"
    echo "🌐 Domain URL: https://$DOMAIN (once DNS is configured)"
fi

echo ""
echo "📝 Next steps:"
echo "1. Configure DNS to point $DOMAIN to your ingress IP"
echo "2. Install cert-manager for automatic SSL certificates"
echo "3. Monitor the deployment: kubectl logs -f deployment/vedic-astrology-app -n $NAMESPACE"
echo "4. Scale if needed: kubectl scale deployment vedic-astrology-app --replicas=5 -n $NAMESPACE"

# Optional: Install cert-manager if not present
if ! kubectl get crd certificates.cert-manager.io &> /dev/null; then
    echo ""
    echo "💡 To install cert-manager for automatic SSL certificates:"
    echo "kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml"
    echo ""
    echo "Then create a ClusterIssuer:"
    cat << 'EOF'
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
fi