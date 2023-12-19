const scrollToTopButton = document.getElementById("scroll-to-top");

scrollToTopButton.onclick = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Show/hide the button based on the scroll position
window.onscroll = () => {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    scrollToTopButton.classList.remove('hidden');
  } else {
    scrollToTopButton.classList.add('hidden');
  }
};
