import React, { useState } from "react";
import axios from "axios";

const Home = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState(null);

  const searchArticles = async (term) => {
    try {
      const response = await axios.get(`/api/articles/search?term=${term}`);
      setArticles(response.data);
      setError(null);
    } catch (error) {
      setError("No articles found with the given term");
      setArticles([]);
    }
  };

  return (
    <div>
      <h1>News Articles</h1>
      <input
        type="text"
        placeholder="Search for articles..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <button onClick={() => searchArticles(searchTerm)}>Search</button>

      {error && <p>{error}</p>}

      {articles.length > 0 ? (
        <ul>
          {articles.map((article) => (
            <li key={article.id}>
              <h2>{article.title}</h2>
              <p><strong>Author:</strong> {article.author}</p>
              <p><strong>Date:</strong> {article.date}</p>
              <p><strong>Summary:</strong> {article.summary}</p>
              <p><strong>Category:</strong> {article.category}</p>
              <p><strong>Sentiment:</strong> {article.sentiment}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No articles found.</p>
      )}
    </div>
  );
};

export default Home;
