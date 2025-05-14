document.addEventListener('DOMContentLoaded', function() {
    // Form submission - add loading state
    const form = document.getElementById('generatorForm');
    const generateBtn = document.getElementById('generateBtn');
    
    if (form) {
        form.addEventListener('submit', function() {
            generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
            generateBtn.disabled = true;
        });
    }
    
    // Copy buttons functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const content = this.getAttribute('data-content');
            copyToClipboard(content, this);
        });
    });
    
    // Copy all content button
    const copyAllBtn = document.getElementById('copyAllBtn');
    
    if (copyAllBtn) {
        copyAllBtn.addEventListener('click', function() {
            // Collect all content
            const instagramCaption = getOutputContent('instagram_caption');
            const facebookPost = getOutputContent('facebook_post');
            const pinterestTitle = getOutputContent('pinterest_title');
            const pinterestDescription = getOutputContent('pinterest_description');
            const pinterestHashtags = getOutputContent('pinterest_hashtags');
            const altText = getOutputContent('alt_text');
            const seoTitle = getOutputContent('seo_title');
            
            // Format all content
            const allContent = `
            === INSTAGRAM CAPTION ===
            ${instagramCaption}
            
            === FACEBOOK POST ===
            ${facebookPost}
            
            === PINTEREST TITLE ===
            ${pinterestTitle}
            
            === PINTEREST DESCRIPTION ===
            ${pinterestDescription}
            
            === PINTEREST HASHTAGS ===
            ${pinterestHashtags}
            
            === ALT TEXT ===
            ${altText}
            
            === SEO PRODUCT TITLE ===
            ${seoTitle}
            `;
            
            copyToClipboard(allContent, copyAllBtn);
        });
    }
    
    // Function to extract content from the page
    function getOutputContent(key) {
        // This is a simplistic way to get the content and might need to be adjusted
        // based on the actual structure of your rendered output
        const elements = document.querySelectorAll(`.content-box`);
        for (let element of elements) {
            if (element.querySelector('p') && element.querySelector('p').textContent.trim()) {
                const paragraphText = element.querySelector('p').textContent.trim();
                const buttonData = element.querySelector('button').getAttribute('data-content');
                
                if (buttonData === paragraphText) {
                    return paragraphText;
                }
            }
        }
        return "";
    }
    
    // Copy to clipboard function
    function copyToClipboard(text, button) {
        navigator.clipboard.writeText(text).then(function() {
            // Visual feedback on successful copy
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i> Copied!';
            button.classList.remove('btn-outline-secondary');
            button.classList.add('btn-success');
            
            // Reset button after 2 seconds
            setTimeout(function() {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-outline-secondary');
            }, 2000);
        }, function(err) {
            console.error('Could not copy text: ', err);
            
            // Visual feedback on error
            button.innerHTML = '<i class="fas fa-times"></i> Failed to copy';
            button.classList.remove('btn-outline-secondary');
            button.classList.add('btn-danger');
            
            // Reset button after 2 seconds
            setTimeout(function() {
                button.innerHTML = '<i class="fas fa-copy"></i> Copy';
                button.classList.remove('btn-danger');
                button.classList.add('btn-outline-secondary');
            }, 2000);
        });
    }
});
