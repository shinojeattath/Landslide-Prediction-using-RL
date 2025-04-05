// Show or hide the add news form
function toggleForm() {
  const form = document.getElementById('addForm');
  form.style.display = form.style.display === 'flex' ? 'none' : 'flex';
}

// Add news item
function addNews() {
  const title = document.getElementById('titleInput').value;
  const content = document.getElementById('contentInput').value;
  const imageUrl = document.getElementById('imageInput').value;

  if (!title || !content || !imageUrl) {
    alert("Please fill in all fields");
    return;
  }

  const newsItem = {
    title,
    content,
    image: imageUrl
  };

  displayNews(newsItem);
  addNewsToList(newsItem);

  // Clear form fields
  document.getElementById('titleInput').value = '';
  document.getElementById('contentInput').value = '';
  document.getElementById('imageInput').value = '';

  toggleForm();
}

// Display news in the left panel
function displayNews(news) {
  const selectedNews = document.getElementById('selectedNews');
  selectedNews.innerHTML = `
    <img src="${news.image}" alt="News Image" class="news-image" />
    <h2 class="news-title">${news.title}</h2>
    <p>${news.content}</p>
  `;
}

// Add news to the right-side list
function addNewsToList(news) {
  const newsList = document.getElementById('newsList');
  const item = document.createElement('div');
  item.className = 'news-item';
  item.innerHTML = `
    <img src="${news.image}" alt="News Image" class="news-image" style="margin-bottom: 8px;" />
    <strong>${news.title}</strong>
  `;
  item.onclick = () => displayNews(news);
  newsList.appendChild(item);
}

// Dummy news items
const dummyNews = [
  {
    title: "Tech Conference 2025 Announced",
    content: "The annual global tech conference will take place in San Francisco, featuring keynote speakers from major tech firms.",
    image: "https://images.unsplash.com/photo-1741986947217-d1a0ecc39149?q=80&w=2066&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    title: "New Species Discovered",
    content: "Scientists have discovered a new species of frog in the Amazon rainforest that glows under UV light.",
    image: "https://images.unsplash.com/photo-1741986947217-d1a0ecc39149?q=80&w=2066&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  },
  {
    title: "Local Art Festival Kicks Off",
    content: "The city square is buzzing with colors as artists from around the world showcase their talent during the 3-day art fest.",
    image: "https://images.unsplash.com/photo-1741986947217-d1a0ecc39149?q=80&w=2066&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
  }
];

// Load dummy news on page load
window.onload = function () {
  dummyNews.forEach(news => {
    addNewsToList(news);
  });

  // Show the first news by default
  displayNews(dummyNews[0]);
};

// Optional: Navbar button actions
function goHome() {
  alert("Going back to home!");
}

function showInfo() {
  alert("This is a simple news showcase app.");
}
