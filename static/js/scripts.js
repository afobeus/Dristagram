function handleImageUpload(event) {
    const image = document.getElementById('post-image');
    image.src = URL.createObjectURL(event.target.files[0]);
    image.style.display = 'block';
}