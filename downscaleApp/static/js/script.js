

document.getElementById('uploadForm').addEventListener('change', function() {
    
    document.getElementById('loadingSpinner').style.display = 'block';

    event.preventDefault();

    this.submit();

});

