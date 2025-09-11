const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = 3000;

// Middlewares
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));
app.set("view engine", "ejs");

// Backend Flask API base URL
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

// Home
app.get("/", (req, res) => {
  res.render("index");
});

// Show Form
app.get("/form", (req, res) => {
  res.render("form", { error: null });
});

// Handle Form Submission -> Flask backend
app.post("/form", async (req, res) => {
  try {
    await axios.post(`${BACKEND_URL}/form`, req.body, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    res.redirect("/success");
  } catch (err) {
    let error = "Submission failed.";
    if (err.response && err.response.data && err.response.data.error) {
      error = err.response.data.error;
    }
    res.render("form", { error });
  }
});

// Success Page
app.get("/success", (req, res) => {
  res.render("success");
});

// Todo Page
app.get("/todo", (req, res) => {
  res.render("todo");
});

// Submit To-do Item -> Flask backend
app.post("/submittodoitem", async (req, res) => {
  try {
    await axios.post(`${BACKEND_URL}/submittodoitem`, req.body, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    res.send("<h2>Todo Item Submitted Successfully!</h2><a href='/todo'>Go Back</a>");
  } catch (err) {
    let errorMessage = "Something went wrong";
    if (err.response && err.response.data && err.response.data.error) {
      errorMessage = err.response.data.error;
    }
    res.send("<h2>Error: " + errorMessage + "</h2>");
  }
});

app.listen(PORT, () => {
  console.log(`Frontend running at http://localhost:${PORT}`);
});
