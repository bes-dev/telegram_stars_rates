class StarsConverter {
    constructor() {
        this.currentRate = 0;
        this.rateData = null;
        this.historyData = null;
        this.chart = null;
        this.init();
    }

    async init() {
        await this.loadRates();
        await this.loadHistory();
        this.setupEventListeners();
        this.updateDisplay();
        this.createChart();
    }

    async loadRates() {
        try {
            const response = await fetch('./rates.json');
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

    async loadHistory() {
        try {
            const response = await fetch('./history.json');
            if (!response.ok) {
                // If history doesn't exist yet, that's OK
                this.historyData = [];
                return;
            }
            
            this.historyData = await response.json();
        } catch (error) {
            console.warn('Failed to load historical data:', error);
            this.historyData = [];
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

    createChart() {
        if (!this.historyData || this.historyData.length === 0) {
            // Hide chart section if no data
            const chartSection = document.querySelector('.chart-section');
            if (chartSection) {
                chartSection.style.display = 'none';
            }
            return;
        }

        const ctx = document.getElementById('rateChart');
        if (!ctx) return;

        // Prepare data for chart
        const labels = this.historyData.map(item => {
            const date = new Date(item.date);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        
        const rates = this.historyData.map(item => item.usdt_per_star);

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Stars → USDT Rate',
                    data: rates,
                    borderColor: '#059669',
                    backgroundColor: 'rgba(5, 150, 105, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#059669',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: (context) => {
                                const value = context.parsed.y;
                                return `$${value.toFixed(6)} USDT per Star`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        grid: {
                            color: '#e2e8f0',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#64748b',
                            maxTicksLimit: 8
                        }
                    },
                    y: {
                        display: true,
                        grid: {
                            color: '#e2e8f0',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#64748b',
                            callback: (value) => `$${value.toFixed(4)}`
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StarsConverter();
});