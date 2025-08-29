document.addEventListener('DOMContentLoaded', function () {
  const nav = document.querySelector("nav");
  const toggle = document.querySelector(".nav-toggle");
  const profileIcon = document.querySelector(".profile-icon");
  const dropdown = document.querySelector(".dropdown");

  toggle.addEventListener("click", () => {
    nav.classList.toggle("show-menu");
  });

  profileIcon.addEventListener("click", (e) => {
    e.preventDefault();
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
  });

  document.addEventListener("click", (e) => {
    if (!profileIcon.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = "none";
    }
  });
});

