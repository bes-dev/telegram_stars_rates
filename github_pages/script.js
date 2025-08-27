class StarsConverter {
    constructor() {
        this.currentRate = 0;
        this.rateData = null;
        this.init();
    }

    async init() {
        await this.loadRates();
        this.setupEventListeners();
        this.updateDisplay();
    }

    async loadRates() {
        try {
            const response = await fetch('./rates.json?v=' + Date.now());
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            this.rateData = await response.json();
            this.currentRate = this.rateData.usdt_per_star || 0;
            
            if (this.currentRate <= 0) {
                throw new Error('Invalid rate data');
            }
            
            this.hideError();
        } catch (error) {
            console.error('Failed to load rates:', error);
            this.showError('Failed to load exchange rates. Please try again later.');
            this.currentRate = 0;
        }
    }


    setupEventListeners() {
        const starsInput = document.getElementById('stars-input');
        const usdtInput = document.getElementById('usdt-input');

        starsInput.addEventListener('input', (e) => {
            const stars = parseFloat(e.target.value) || 0;
            const usdt = stars * this.currentRate;
            usdtInput.value = usdt > 0 ? usdt.toFixed(6) : '';
        });

        usdtInput.addEventListener('input', (e) => {
            const usdt = parseFloat(e.target.value) || 0;
            const stars = this.currentRate > 0 ? usdt / this.currentRate : 0;
            starsInput.value = stars > 0 ? Math.round(stars) : '';
        });
    }

    updateDisplay() {
        if (!this.rateData) return;

        // Main rate display
        const rateValue = document.getElementById('rate-value');
        if (this.currentRate > 0) {
            rateValue.textContent = `$${this.currentRate.toFixed(6)}`;
        } else {
            rateValue.textContent = 'N/A';
        }

        // Last updated
        const lastUpdated = document.getElementById('last-updated');
        if (this.rateData.timestamp) {
            const date = new Date(this.rateData.timestamp);
            lastUpdated.textContent = date.toLocaleString();
        }

        // Transaction count
        const txCount = document.getElementById('tx-count');
        if (this.rateData.fragment_raw?.transactions_count) {
            txCount.textContent = this.rateData.fragment_raw.transactions_count;
        }

        // Stats
        if (this.rateData.fragment_raw) {
            const fragment = this.rateData.fragment_raw;
            
            document.getElementById('min-rate').textContent = 
                fragment.min_rate ? `$${(fragment.min_rate * this.rateData.usdt_per_ton).toFixed(6)}` : '-';
            
            document.getElementById('max-rate').textContent = 
                fragment.max_rate ? `$${(fragment.max_rate * this.rateData.usdt_per_ton).toFixed(6)}` : '-';
            
            document.getElementById('median-rate').textContent = 
                fragment.median_rate ? `$${(fragment.median_rate * this.rateData.usdt_per_ton).toFixed(6)}` : '-';
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    hideError() {
        const errorDiv = document.getElementById('error-message');
        errorDiv.style.display = 'none';
    }

}

// Copy to clipboard function for API examples
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show temporary feedback
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = '✅';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            const button = event.target;
            const originalText = button.textContent;
            button.textContent = '✅';
            setTimeout(() => {
                button.textContent = originalText;
            }, 2000);
        } catch (err) {
            console.error('Fallback copy failed: ', err);
        }
        document.body.removeChild(textArea);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StarsConverter();
});