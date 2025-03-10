import express from "express";
import {
  createItem,
  getAllItems,
  getItemById,
  updateItem,
  deleteItem
} from "../controllers/itemController.js";

const router = express.Router();

// Item routes
router.post("/create", createItem);        // Create a new item
router.get("/", getAllItems);        // Get all items
router.get("/:id", getItemById);     // Get a specific item by ID
router.put("/:id", updateItem);      // Update an item
router.delete("/:id", deleteItem);   // Delete an item

export default router;
