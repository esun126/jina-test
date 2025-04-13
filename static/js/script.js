// Jina AI Document Learning Web Interface Scripts

document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const documentForm = document.getElementById('document-form');
    const questionForm = document.getElementById('question-form');
    const clearSessionBtn = document.getElementById('clear-session');
    
    // Input elements
    const urlInput = document.getElementById('url');
    const apiKeyInput = document.getElementById('api-key');
    const questionInput = document.getElementById('question');
    
    // Display elements
    const documentInfoCard = document.getElementById('document-info-card');
    const documentInfo = document.getElementById('document-info');
    const questionCard = document.getElementById('question-card');
    const answerCard = document.getElementById('answer-card');
    const answer = document.getElementById('answer');
    const sources = document.getElementById('sources');
    
    // Process document form submission
    documentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        const apiKey = apiKeyInput.value.trim();
        
        if (!url || !apiKey) {
            alert('Please enter both URL and API key');
            return;
        }
        
        // Show loading indicator
        const submitBtn = documentForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = 'Processing... <span class="loading"></span>';
        submitBtn.disabled = true;
        
        // Send request to process document
        fetch('/process_document', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                api_key: apiKey
            })
        })
        .then(response => response.json())
        .then(data => {
            // Reset button
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            
            if (data.success) {
                // Display document information
                displayDocumentInfo(data.document);
                
                // Show question form
                questionCard.style.display = 'block';
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            // Reset button
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            
            alert('Error: ' + error.message);
        });
    });
    
    // Ask question form submission
    questionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const question = questionInput.value.trim();
        
        if (!question) {
            alert('Please enter a question');
            return;
        }
        
        // Show loading indicator
        const submitBtn = questionForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = 'Asking... <span class="loading"></span>';
        submitBtn.disabled = true;
        
        // Send request to ask question
        fetch('/ask_question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question
            })
        })
        .then(response => response.json())
        .then(data => {
            // Reset button
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            
            if (data.success) {
                // Display answer
                displayAnswer(data.answer, data.sources);
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            // Reset button
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            
            alert('Error: ' + error.message);
        });
    });
    
    // Clear session button click
    clearSessionBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear the current session? This will remove all processed documents.')) {
            fetch('/clear_session', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reset UI
                    documentInfoCard.style.display = 'none';
                    questionCard.style.display = 'none';
                    answerCard.style.display = 'none';
                    documentInfo.innerHTML = '';
                    answer.innerHTML = '';
                    sources.innerHTML = '';
                    
                    // Clear form inputs
                    urlInput.value = '';
                    questionInput.value = '';
                    
                    alert('Session cleared successfully');
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                alert('Error: ' + error.message);
            });
        }
    });
    
    // Function to display document information
    function displayDocumentInfo(document) {
        documentInfo.innerHTML = `
            <div class="document-title">${document.title}</div>
            <div class="document-url"><a href="${document.url}" target="_blank">${document.url}</a></div>
            <div>Number of chunks: ${document.num_chunks}</div>
            <div class="document-preview">${document.content_preview}</div>
        `;
        
        documentInfoCard.style.display = 'block';
    }
    
    // Function to display answer and sources
    function displayAnswer(answerText, sourcesData) {
        answer.innerHTML = answerText;
        
        let sourcesHtml = '<h6>Sources:</h6><ul>';
        
        sourcesData.forEach((source, index) => {
            sourcesHtml += `
                <li class="source-item">
                    <a href="${source.url}" target="_blank">${source.title}</a>
                </li>
            `;
        });
        
        sourcesHtml += '</ul>';
        sources.innerHTML = sourcesHtml;
        
        answerCard.style.display = 'block';
    }
});
