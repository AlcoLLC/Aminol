document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('cvFile');
    
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            uploadArea.innerHTML = `<i class="fa-solid fa-file"></i> ${file.name}`;
            uploadArea.style.color = '#28315e';
        }
    });
    
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#b4b7d4';
        uploadArea.style.backgroundColor = '#e7f3ff';
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#b4b7d425';
        uploadArea.style.backgroundColor = '#f6f9ff';
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#b4b7d425';
        uploadArea.style.backgroundColor = '#f6f9ff';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });




     const textAreaDiv = document.querySelector('.text-area');
    const hiddenTextarea = document.getElementById('motivationLetter');
    
    textAreaDiv.addEventListener('click', function() {
        hiddenTextarea.style.display = 'block';
        textAreaDiv.style.display = 'none';
        hiddenTextarea.focus();
    });
    
    hiddenTextarea.addEventListener('blur', function() {
        if (hiddenTextarea.value.trim() === '') {
            textAreaDiv.style.display = 'block';
            hiddenTextarea.style.display = 'none';
        } else {
            textAreaDiv.innerHTML = hiddenTextarea.value.replace(/\n/g, '<br>');
            textAreaDiv.style.display = 'block';
            hiddenTextarea.style.display = 'none';
        }
    });
    
});

