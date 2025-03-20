import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import sellerRoutes from "./routes/sellerRoutes.js";
import itemRoutes from "./routes/itemRoutes.js";
import orderRoutes from "./routes/orderRoutes.js";
// import uploadRoutes from "./routes/uploadRoutes.js";
import shopRoutes from "./routes/shopRoutes.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

const corsOptions = {
  origin: ["http://localhost:5173"], // Frontend URL
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true // Allow credentials like cookies or tokens
};

app.use(cors(corsOptions));
app.use(express.json());

// Routes
app.use("/", sellerRoutes);
app.use("/", itemRoutes);
app.use("/", orderRoutes);
app.use("/", shopRoutes);
// app.use("/", uploadRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({ error: err.message || "Internal Server Error" });
});

app.listen(PORT, () => {
  console.log(`Server: Running on port ${PORT}`);
});
