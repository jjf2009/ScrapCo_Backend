import express from "express";
import prisma from "../prismaClient.js";

const router = express.Router();

// Post data
router.post("/addItem", async (req, res) => {
  const { name, images, points, stock, category, description, company } = req.body;
  try {
    const item = await prisma.shopItem.create({
      data: {
        name,
        images,
        points,
        stock,
        category,
        description,
        company,
      },
    });
    console.log("Item created:", item);
    res.status(201).json(item);
  } catch (error) {
    console.error("Error creating item:", error);
    res.status(500).json({ message: "Failed to create item", error: error.message });
  }
});

// Get shop items
router.get("/shop/allItems", async (req, res) => {
  try {
    console.log("Request received at /shop");
    const data = await prisma.shopItem.findMany();
    if (data.length === 0) {
      console.log("No items found");
      return res.status(404).json({ message: "No items found" });
    }
    console.log("Fetched data:", data);
    res.status(200).json(data);
  } catch (error) {
    console.error("Error fetching items:", error);
    res.status(500).json({ message: "Failed to fetch items", error: error.message });
  }
});

export default router;
