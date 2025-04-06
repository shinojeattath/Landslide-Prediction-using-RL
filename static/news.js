let featuredNews = {
    title: "Tech Conference 2025 Announced",
    content: "The global tech conference will be held in San Francisco, showcasing the latest innovations in AI, Robotics, and Quantum Computing.",
    image: "https://via.placeholder.com/600x300/007bff/ffffff?text=Tech+Conference+2025"
  };
  
  let otherNews = [
    {
      title: "AI Revolution",
      content: "AI is transforming industries worldwide with smart automation and predictive capabilities.",
      image: "https://via.placeholder.com/600x300/ffcc00/000000?text=AI+Revolution"
    },
    {
      title: "SpaceX Launch",
      content: "SpaceX successfully launched its Starship prototype into orbit, marking a milestone in reusable rockets.",
      image: "https://via.placeholder.com/600x300/66ccff/000000?text=SpaceX+Launch"
    },
    {
      title: "Climate Action Summit",
      content: "Leaders from over 100 countries gathered to discuss urgent actions to combat climate change.",
      image: "https://via.placeholder.com/600x300/99cc99/000000?text=Climate+Summit"
    },
    {
      title: "Global Markets Today",
      content: "Stocks showed mixed results amid inflation concerns and tech sector volatility.",
      image: "https://via.placeholder.com/600x300/ff6666/000000?text=Market+Update"
    },
    {
      title: "Education Tech Boom",
      content: "EdTech startups are seeing a surge in investment as remote learning becomes the norm.",
      image: "https://via.placeholder.com/600x300/cc99ff/000000?text=EdTech+Boom"
    }
  ];
  
  function renderFeaturedNews() {
    const left = document.getElementById("selectedNews");
    left.innerHTML = `
      <img src="${featuredNews.image}" class="news-image" alt="news"/>
      <h2 class="news-title">${featuredNews.title}</h2>
      <p>${featuredNews.content}</p>
    `;
  }
  
  function renderNewsList() {
    const list = document.getElementById("newsList");
    list.innerHTML = "";
  
    otherNews.forEach((news, index) => {
      const item = document.createElement("div");
      item.className = "news-item";
      item.textContent = news.title;
      item.onclick = () => swapNews(index);
      list.appendChild(item);
    });
  }
  
  function swapNews(index) {
    const selected = otherNews[index];
    otherNews[index] = featuredNews;
    featuredNews = selected;
    renderFeaturedNews();
    renderNewsList();
  }
  
  function toggleForm() {
    const form = document.getElementById("addForm");
    form.style.display = form.style.display === "flex" ? "none" : "flex";
  }
  
  function addNews() {
    const title = document.getElementById("titleInput").value.trim();
    const content = document.getElementById("contentInput").value.trim();
    const image = document.getElementById("imageInput").value.trim();
  
    if (!title || !content || !image) {
      alert("Please fill all fields!");
      return;
    }
  
    otherNews.push({ title, content, image });
  
    // Reset form
    document.getElementById("titleInput").value = "";
    document.getElementById("contentInput").value = "";
    document.getElementById("imageInput").value = "";
  
    toggleForm();
    renderNewsList();
  }
  
  function goHome() {
    alert("Redirecting to homepage...");
  }
  
  function showInfo() {
    alert("This is a simple news showcase app. Click on a headline to view the full article.");
  }
  
  // Initialize
  renderFeaturedNews();
  renderNewsList();
  