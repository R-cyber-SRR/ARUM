// Banner Generator JavaScript
class BannerGenerator {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupValidation();
    }

    initializeElements() {
        // Form elements
        this.form = {
            text: document.getElementById('bannerText'),
            style: document.getElementById('bannerStyle'),
            textColor: document.getElementById('textColor'),
            fontSize: document.getElementById('fontSize'),
            width: document.getElementById('width'),
            height: document.getElementById('height')
        };

        // UI elements
        this.preview = document.getElementById('bannerPreview');
        this.generateBtn = document.querySelector('.btn');
        this.loadingOverlay = document.querySelector('.loading-overlay');
        
        // Messages
        this.errorMessage = document.querySelector('.error-message');
        this.successMessage = document.querySelector('.success-message');
    }

    bindEvents() {
        // Generate button click
        this.generateBtn.addEventListener('click', () => this.generateBanner());

        // Real-time preview updates
        this.form.width.addEventListener('input', () => this.updatePreviewDimensions());
        this.form.height.addEventListener('input', () => this.updatePreviewDimensions());
        
        // Input validation
        Object.values(this.form).forEach(input => {
            if (input.type === 'number') {
                input.addEventListener('input', (e) => this.validateNumberInput(e.target));
            }
        });
    }

    setupValidation() {
        this.validation = {
            text: {
                min: 1,
                max: 100,
                required: true
            },
            fontSize: {
                min: 12,
                max: 120
            },
            width: {
                min: 300,
                max: 2000
            },
            height: {
                min: 100,
                max: 1000
            }
        };
    }

    validateNumberInput(input) {
        const rules = this.validation[input.id];
        if (!rules) return true;

        const value = parseInt(input.value);
        if (value < rules.min) input.value = rules.min;
        if (value > rules.max) input.value = rules.max;
    }

    validateForm() {
        let isValid = true;
        const errors = [];

        if (!this.form.text.value.trim() && this.validation.text.required) {
            errors.push('Banner text is required');
            isValid = false;
        }

        Object.keys(this.validation).forEach(field => {
            if (this.form[field] && this.form[field].type === 'number') {
                const value = parseInt(this.form[field].value);
                const rules = this.validation[field];

                if (value < rules.min || value > rules.max) {
                    errors.push(`${field} must be between ${rules.min} and ${rules.max}`);
                    isValid = false;
                }
            }
        });

        if (!isValid) {
            this.showError(errors.join(', '));
        }

        return isValid;
    }

    async generateBanner() {
        if (!this.validateForm()) return;

        this.showLoading(true);
        
        const bannerData = {
            text: this.form.text.value,
            style: this.form.style.value,
            textColor: this.form.textColor.value,
            fontSize: parseInt(this.form.fontSize.value),
            width: parseInt(this.form.width.value),
            height: parseInt(this.form.height.value)
        };

        try {
            const response = await fetch('/generate-banner', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(bannerData)
            });

            if (!response.ok) throw new Error('Failed to generate banner');

            const data = await response.json();
            this.updatePreview(data.banner_url);
            this.showSuccess('Banner generated successfully!');
        } catch (error) {
            this.showError('Failed to generate banner. Please try again.');
            console.error('Error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    updatePreview(bannerUrl) {
        this.preview.style.backgroundImage = `url(${bannerUrl})`;
        this.updatePreviewDimensions();
    }

    updatePreviewDimensions() {
        this.preview.style.width = `${this.form.width.value}px`;
        this.preview.style.height = `${this.form.height.value}px`;
    }

    showLoading(show) {
        this.loadingOverlay.style.display = show ? 'flex' : 'none';
        this.generateBtn.disabled = show;
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.style.display = 'block';
        this.successMessage.style.display = 'none';
        setTimeout(() => {
            this.errorMessage.style.display = 'none';
        }, 5000);
    }

    showSuccess(message) {
        this.successMessage.textContent = message;
        this.successMessage.style.display = 'block';
        this.errorMessage.style.display = 'none';
        setTimeout(() => {
            this.successMessage.style.display = 'none';
        }, 3000);
    }
}

// Initialize the banner generator when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.bannerGenerator = new BannerGenerator();
});