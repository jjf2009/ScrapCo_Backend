import express from "express";
import { signupSeller, loginSeller } from "../controllers/sellerController.js";

const router = express.Router();

// Seller Signup
router.post("/register", signupSeller);

// Seller Login
router.post("/login", loginSeller);

export default router;
