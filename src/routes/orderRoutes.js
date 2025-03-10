import express from "express";
import { createOrder, getOrdersByUserId } from "../controllers/orderController.js";

const router = express.Router();

router.post("/", createOrder);         // Create a new order
router.get("/:user_id", getOrdersByUserId);  // Get all orders by user ID

export default router;
