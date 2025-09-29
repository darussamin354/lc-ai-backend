<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>LC AI Pro</title>

  <!-- React & ReactDOM via CDN -->
  <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>

  <!-- Babel untuk transpile JSX dalam browser -->
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <!-- Styling -->
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #0d0d0d;
      color: #f5c542;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      text-align: center;
    }
    .card {
      background: #1a1a1a;
      padding: 2rem;
      border-radius: 1rem;
      box-shadow: 0 0 20px rgba(245, 197, 66, 0.4);
      max-width: 450px;
      width: 100%;
    }
    h1 {
      color: #f5c542;
      margin-bottom: 1rem;
    }
    input[type="file"] {
      margin: 1rem 0;
      color: #f5c542;
    }
    button {
      background: #f5c542;
      border: none;
      color: #0d0d0d;
      font-weight: bold;
      padding: 0.75rem 1.5rem;
      border-radius: 0.5rem;
      cursor: pointer;
      margin-top: 1rem;
    }
    button:disabled {
      background: #999;
      cursor: not-allowed;
    }
    button:hover:not(:disabled) {
      background: #ffdb70;
    }
    .result {
      margin-top: 1.5rem;
      text-align: left;
      background: #0d0d0d;
      padding: 1rem;
      border-radius: 0.5rem;
      border: 1px solid #f5c542;
    }
    .loading {
      margin-top: 1rem;
      color: #ffdb70;
    }
  </style>
</head>
<body>
  <div id="root"></div>

  <!-- React code -->
  <script type="text/babel">
    function App() {
      const [result, setResult] = React.useState(null);
      const [file, setFile] = React.useState(null);
      const [loading, setLoading] = React.useState(false);

      async function handleAnalyze() {
        if (!file) {
          alert("Upload screenshot dulu!");
          return;
        }
        setLoading(true);

        const fd = new FormData();
        fd.append("file", file);
        fd.append("pair", "EUR/USD");
        fd.append("timeframe", "H1");
        fd.append("current_price", "3391.1");

        try {
          const res = await fetch("https://lc-ai-backend-2.onrender.com/analyze", {
            method: "POST",
            body: fd
          });
          const data = await res.json();
          setResult(data);
        } catch (err) {
          alert("Error connect to backend");
          console.error(err);
        } finally {
          setLoading(false);
        }
      }

      return (
        <div className="card">
          <h1>⚡ LC AI Pro ⚡</h1>
          <p>Upload screenshot untuk analisis AI (connected to backend)</p>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Run AI Analysis"}
          </button>

          {loading && <p className="loading">Sedang analisis... tunggu sebentar ⚡</p>}

          {result && (
            <div className="result">
              <p><strong>Pair:</strong> {result.pair}</p>
              <p><strong>Timeframe:</strong> {result.timeframe}</p>
              <p><strong>Entry Price:</strong> {result.analysis.entry_price}</p>
              <p><strong>Take Profit:</strong> {result.analysis.take_profit}</p>
              <p><strong>Stop Loss:</strong> {result.analysis.stop_loss}</p>
              <p><strong>Confidence:</strong> {result.analysis.confidence}%</p>
            </div>
          )}
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById("root")).render(<App />);
  </script>
</body>
</html>
