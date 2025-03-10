import express from "express";
import { createProduct, getAllProducts, getProductById, updateProduct, deleteProduct } from "../controllers/productController.js";

const router = express.Router();

router.post("/", createProduct);       // Create a new product
router.get("/", getAllProducts);       // Get all products
router.get("/:id", getProductById);    // Get a product by ID
router.put("/:id", updateProduct);     // Update a product
router.delete("/:id", deleteProduct);  // Delete a product

export default router;
