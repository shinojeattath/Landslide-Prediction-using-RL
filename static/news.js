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
    title: "Wayanad, Kerala - 30 July 2024",
    content: "On July 30, 2024, Wayanad in Kerala witnessed India’s worst-ever landslide, devastating the villages of Punchirimattam, Chooralmala and Mundakkai. The scale of destruction was unimaginable, with over 231 people confirmed dead, while body parts of 218 others have been recovered. After this massive tragedy, life struggles to return to normal, with many areas abandoned and debris still scattered across a once-thriving landscape.\n\nIn Chooralmala, the local post office is one of the few structures still operating. Packages pile up daily, mostly addressed to the missing or deceased. Outside, the police patrol to prevent curious disaster tourists from taking selfies, while another team guards ruined homes against theft.",
    image: "https://th-i.thgim.com/public/incoming/fycxxz/article68525295.ece/alternates/FREE_1200/image%2010.jpeg"
  },
  {
    title: "Shirur, Karnataka - 16 July 2024",
    content: "On the morning of July 16, 2024, a significant landslide occurred in Shirur of Uttara Kannada district, Karnataka, India. The landslide claimed seven lives, leaving one person missing and severely disrupting the transport network by blocking National Highway 66. The displaced debris travelled 180m across the highway and into the Gangavali River, causing a significant splash and damaging structures on the opposite bank. The event, characterised by a rotational slip, was triggered by a combination of anthropogenic activities and intense rainfall. The construction of National Highway 66, which involved the removal of the slope's toe without adequate protection for the excavation, significantly destabilised the area. On 15th July, the rain gauge in Ankola recorded rainfall of 260 ​mm. The accumulated rainfall calculated for Shirur using Inverse Distance Weightage (IDW) for the storm period of 4 days was 198 ​mm, which increased the pore water pressure within the soil, weakening its shear strength and leading to slope failure. This incident underscores the need for further analysis and the implementation of appropriate mitigation measures, as the region remains at risk for future landslides. The Shirur landslide serves as a critical reminder of the dynamic nature of such disasters, particularly when human activities exacerbate natural hazards.",
    image: "https://images.deccanherald.com/deccanherald%2F2024-09-23%2Fznc3w8m0%2FiStock-1759143984.jpg"
  },
  {
    title: "Kavalappara, Kerala - 08 August 2019",
    content: "Month of August experienced heavy rainfall on the Western Ghat mountain ranges of southern India in 2019 with exceptionally heavy rainfall i.e. 400% over the normal average during 5 cumulative days resulting in the devastating landslide on 8th August 2019. It was difficult to estimate the actual loss however 69 casualties, 39 completely damaged houses along with roads, utilities and other infrastructure damages were recorded during our survey. The children and adults who managed to escape their death were completely traumatised and were unable to talk. Through field and desk geoscientific investigation it was found that the mismanagement of land use, unscientific slope modification, disruption of free flow of drainage, added with huge amounts of water due to heavy rainfall leading to supersaturation of highly weathered and structurally disposed debris material overlying Archaean bedrock and toe erosion due to flooded river resulted in this landslide. Although the slide happened in a rapid way but precursory signature as cracking and rumbling sound was heard before the actual event. However people were trapped and could not go away as their escape root was flooded. The landslide happened in the northern trifurcated downslope segments as the three 1st order drainage courses carried the discharge of debris and water.",
    image: "https://therenaissanceofficial.org/wp-content/uploads/2023/11/1382732-kavalappara-landslide.webp"
  },
  {
    title: "Aizawl, Mizoram - May 2024",
    content: "In May 2024, Aizawl, the capital of Mizoram, experienced devastating landslides and floods, particularly in the aftermath of Cyclone Remal, leading to numerous casualties and widespread destruction. Rescue operations were launched to locate missing persons, with the Mizoram State Disaster Management Authority (MSDMA) coordinating efforts. The landslides and floods caused significant damage to property, including houses, cemeteries, and infrastructure, with reports of collapsed houses and worker camps in areas like Melthum and Hlimen. Heavy rainfall and the geological conditions of the region, including steep slopes and unconsolidated sedimentary formations, are considered major contributing factors to the landslides.  The death toll in Aizawl district rose to 28, with 27 bodies recovered and 6 still missing, according to reports from the Mizoram State Disaster Management Authority. The incident highlighted the vulnerability of the region to natural disasters, particularly landslides, and the need for effective disaster management and mitigation strategies.",
    image: "https://images.indianexpress.com/2024/05/PTI05_28_2024_000103B.jpg"
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
