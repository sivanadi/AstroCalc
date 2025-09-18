#!/bin/bash
# SSL Certificate Generation Script for Vedic Astrology Calculator
# Supports both self-signed certificates and Let's Encrypt

set -e

DOMAIN=${1:-"vedic-astrology.local"}
SSL_DIR=${2:-"/etc/ssl/vedic-astrology"}
EMAIL=${3:-"admin@${DOMAIN}"}

echo "🔐 SSL Certificate Setup for Vedic Astrology Calculator"
echo "======================================================="
echo "Domain: $DOMAIN"
echo "SSL Directory: $SSL_DIR"

# Create SSL directory
sudo mkdir -p "$SSL_DIR"
cd "$SSL_DIR"

# Function to generate self-signed certificate
generate_self_signed() {
    echo "🔑 Generating self-signed certificate..."
    
    # Generate private key
    sudo openssl genrsa -out key.pem 2048
    
    # Generate certificate signing request
    sudo openssl req -new -key key.pem -out csr.pem -subj "/C=US/ST=State/L=City/O=Organization/OU=IT/CN=$DOMAIN"
    
    # Generate self-signed certificate
    sudo openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem
    
    # Create chain file (same as cert for self-signed)
    sudo cp cert.pem chain.pem
    
    # Set permissions
    sudo chmod 600 key.pem
    sudo chmod 644 cert.pem chain.pem csr.pem
    
    echo "✅ Self-signed certificate generated successfully!"
    echo "📁 Files created in: $SSL_DIR"
    echo "   - key.pem (private key)"
    echo "   - cert.pem (certificate)"
    echo "   - chain.pem (certificate chain)"
    echo "   - csr.pem (certificate signing request)"
}

# Function to setup Let's Encrypt
setup_letsencrypt() {
    echo "🌐 Setting up Let's Encrypt certificate..."
    
    # Check if certbot is installed
    if ! command -v certbot &> /dev/null; then
        echo "📦 Installing certbot..."
        
        # Install based on OS
        if [[ -f /etc/debian_version ]]; then
            sudo apt-get update
            sudo apt-get install -y certbot python3-certbot-nginx python3-certbot-apache
        elif [[ -f /etc/redhat-release ]]; then
            sudo yum install -y certbot python3-certbot-nginx python3-certbot-apache
        else
            echo "❌ Unsupported OS for automatic certbot installation"
            echo "Please install certbot manually and run this script again"
            exit 1
        fi
    fi
    
    # Choose web server
    echo "Select web server:"
    echo "1) Nginx"
    echo "2) Apache"
    echo "3) Standalone (manual configuration required)"
    read -p "Enter choice [1-3]: " webserver_choice
    
    case $webserver_choice in
        1)
            sudo certbot certonly --nginx -d "$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive
            ;;
        2)
            sudo certbot certonly --apache -d "$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive
            ;;
        3)
            sudo certbot certonly --standalone -d "$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
    
    # Copy certificates to our SSL directory
    LETSENCRYPT_DIR="/etc/letsencrypt/live/$DOMAIN"
    if [[ -d "$LETSENCRYPT_DIR" ]]; then
        sudo cp "$LETSENCRYPT_DIR/privkey.pem" "$SSL_DIR/key.pem"
        sudo cp "$LETSENCRYPT_DIR/cert.pem" "$SSL_DIR/cert.pem"
        sudo cp "$LETSENCRYPT_DIR/chain.pem" "$SSL_DIR/chain.pem"
        sudo cp "$LETSENCRYPT_DIR/fullchain.pem" "$SSL_DIR/fullchain.pem"
        
        sudo chmod 600 "$SSL_DIR/key.pem"
        sudo chmod 644 "$SSL_DIR/cert.pem" "$SSL_DIR/chain.pem" "$SSL_DIR/fullchain.pem"
        
        echo "✅ Let's Encrypt certificate installed successfully!"
        
        # Setup auto-renewal
        setup_auto_renewal
    else
        echo "❌ Let's Encrypt certificate generation failed"
        exit 1
    fi
}

# Function to setup certificate auto-renewal
setup_auto_renewal() {
    echo "🔄 Setting up automatic certificate renewal..."
    
    # Create renewal script
    cat << 'EOF' | sudo tee /usr/local/bin/renew-vedic-astrology-cert.sh > /dev/null
#!/bin/bash
# Auto-renewal script for Vedic Astrology Calculator SSL certificate

certbot renew --quiet

# Copy renewed certificates
if [[ -d "/etc/letsencrypt/live/DOMAIN_PLACEHOLDER" ]]; then
    cp "/etc/letsencrypt/live/DOMAIN_PLACEHOLDER/privkey.pem" "SSL_DIR_PLACEHOLDER/key.pem"
    cp "/etc/letsencrypt/live/DOMAIN_PLACEHOLDER/cert.pem" "SSL_DIR_PLACEHOLDER/cert.pem"
    cp "/etc/letsencrypt/live/DOMAIN_PLACEHOLDER/chain.pem" "SSL_DIR_PLACEHOLDER/chain.pem"
    cp "/etc/letsencrypt/live/DOMAIN_PLACEHOLDER/fullchain.pem" "SSL_DIR_PLACEHOLDER/fullchain.pem"
    
    chmod 600 "SSL_DIR_PLACEHOLDER/key.pem"
    chmod 644 "SSL_DIR_PLACEHOLDER/cert.pem" "SSL_DIR_PLACEHOLDER/chain.pem" "SSL_DIR_PLACEHOLDER/fullchain.pem"
    
    # Reload web server
    systemctl reload nginx || systemctl reload apache2 || true
fi
EOF
    
    # Replace placeholders
    sudo sed -i "s|DOMAIN_PLACEHOLDER|$DOMAIN|g" /usr/local/bin/renew-vedic-astrology-cert.sh
    sudo sed -i "s|SSL_DIR_PLACEHOLDER|$SSL_DIR|g" /usr/local/bin/renew-vedic-astrology-cert.sh
    
    # Make executable
    sudo chmod +x /usr/local/bin/renew-vedic-astrology-cert.sh
    
    # Add to crontab (run twice daily)
    (sudo crontab -l 2>/dev/null; echo "0 */12 * * * /usr/local/bin/renew-vedic-astrology-cert.sh") | sudo crontab -
    
    echo "✅ Auto-renewal setup complete!"
    echo "📅 Certificate will be checked for renewal twice daily"
}

# Function to verify certificate
verify_certificate() {
    echo "🔍 Verifying SSL certificate..."
    
    if [[ -f "$SSL_DIR/cert.pem" && -f "$SSL_DIR/key.pem" ]]; then
        # Check if certificate and key match
        cert_hash=$(sudo openssl x509 -in "$SSL_DIR/cert.pem" -noout -modulus | openssl md5)
        key_hash=$(sudo openssl rsa -in "$SSL_DIR/key.pem" -noout -modulus | openssl md5)
        
        if [[ "$cert_hash" == "$key_hash" ]]; then
            echo "✅ Certificate and private key match"
            
            # Show certificate details
            echo "📋 Certificate details:"
            sudo openssl x509 -in "$SSL_DIR/cert.pem" -noout -subject -dates -issuer
        else
            echo "❌ Certificate and private key do not match!"
            exit 1
        fi
    else
        echo "❌ Certificate files not found!"
        exit 1
    fi
}

# Main menu
echo ""
echo "Select SSL setup method:"
echo "1) Generate self-signed certificate (for development/testing)"
echo "2) Setup Let's Encrypt certificate (for production)"
echo "3) Verify existing certificate"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        generate_self_signed
        verify_certificate
        ;;
    2)
        if [[ "$DOMAIN" == "vedic-astrology.local" ]]; then
            echo "❌ Let's Encrypt requires a real domain name"
            echo "Please run: $0 your-domain.com"
            exit 1
        fi
        setup_letsencrypt
        verify_certificate
        ;;
    3)
        verify_certificate
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 SSL setup complete!"
echo "📝 Next steps:"
echo "1. Update your web server configuration to use the certificates"
echo "2. Test the SSL configuration"
echo "3. Ensure firewall allows HTTPS traffic (port 443)"

# Web server configuration hints
echo ""
echo "💡 Web server configuration:"
echo "Nginx: Update ssl_certificate and ssl_certificate_key paths in nginx.conf"
echo "Apache: Update SSLCertificateFile and SSLCertificateKeyFile in your VirtualHost"
echo ""
echo "Certificate files location: $SSL_DIR"