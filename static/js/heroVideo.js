export default () => {
    const heroVideo = document.getElementById('hero-video');

    if (!heroVideo) return;

    // Pause the video initially (even though autoplay is set)
    heroVideo.pause();

    // Start playing after 5 seconds
    setTimeout(heroVideo.play, 5000);

    // Add hover effect - pause on hover
    heroVideo.addEventListener('mouseenter', heroVideo.pause);

    // Resume playing when mouse leaves
    heroVideo.addEventListener('mouseleave', heroVideo.play);
};