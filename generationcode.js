// Add event listener to the form
document.getElementById('bannerForm').addEventListener('submit', generateBanner);

async function generateBanner(event) {
    // Prevent the default form submission
    event.preventDefault();
    
    // Show loading state
    const generateButton = document.querySelector('button[type="submit"]');
    const originalButtonText = generateButton.textContent;
    generateButton.textContent = 'Generating...';
    generateButton.disabled = true;

    try {
        // Create FormData from the form
        const formData = new FormData();
        formData.append('text', document.getElementById('bannerText').value || '');
        formData.append('width', document.getElementById('width').value || '1200');
        formData.append('height', document.getElementById('height').value || '1300');
        formData.append('fontSize', document.getElementById('fontSize').value || '56');
        formData.append('textColor', document.getElementById('textColor').value || '#FF0000');

        // Make the API call
        const response = await fetch('/generate-banner', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Update preview with new banner
            const previewImg = document.getElementById('preview');
            if (previewImg) {
                // Add cache-busting parameter
                previewImg.src = `${data.path}?t=${new Date().getTime()}`;
                previewImg.style.display = 'block';
            }
        } else {
            throw new Error(data.error || 'Failed to generate banner');
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Error generating banner: ${error.message}`);
    } finally {
        // Reset button state
        generateButton.textContent = originalButtonText;
        generateButton.disabled = false;
    }
}

// Add preview image error handling
document.getElementById('preview')?.addEventListener('error', function(e) {
    console.error('Error loading preview image');
    this.style.display = 'none';
    alert('Error loading preview image');
});