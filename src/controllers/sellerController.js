import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
import prisma from "../prismaClient.js";
import validator from "validator";

const { isEmail, isMobilePhone } = validator;

dotenv.config();

// Seller Signup Controller
export const signupSeller = async (req, res) => {
    try {
        const {
            fullName, phone, email, password, permAddress, sellerRole, gstNumber, licenseNumber
        } = req.body;

        let orgAddress = null;
        let orgName = null;

        if (sellerRole === "ORGANISATION") {
            orgName = req.body.orgName;
            orgAddress = req.body.orgAddress;
        }

        // Field validation
        if (!fullName || !phone || !email || !password || !permAddress || !sellerRole) {
            return res.status(400).json({ message: "All fields are required" });
        }
        if (sellerRole === "ORGANISATION" && (!orgName || !orgAddress)) {
            return res.status(400).json({ message: "All fields are required" });
        }
        // if (!isEmail(email) || !isMobilePhone(phone, 'any')) {
        //     return res.status(400).json({ message: "Enter valid credentials" });
        // }
        if (password.length < 6) {
            return res.status(400).json({ message: "Password should be at least 6 characters long" });
        }

        // Hashing password
        const hashedPassword = bcrypt.hashSync(password, 8);

        try {
            const user = await prisma.user.create({
                data: {
                    fullName,
                    phone,
                    email,
                    passwordHash: hashedPassword,
                    permAddress,
                    sellerRole,
                    gstNo: gstNumber || undefined,
                    licNum: licenseNumber || undefined,
                    orgName: orgName || undefined,
                    orgAddress: orgAddress || undefined
                }
            });

            const token = jwt.sign({ id: user.userId }, process.env.JWT_SECRET, { expiresIn: '8h' });

            console.log("User successfully created");
            res.json({ token });

        } catch (error) {
            res.status(500).json({ message: `Error creating user: ${error.message}` });
        }

    } catch (error) {
        res.status(500).json({ message: `Server error: ${error.message}` });
    }
};

// Seller Login Controller
export const loginSeller = async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({ message: "Email and password are required" });
        }

        const user = await prisma.user.findUnique({ where: { email } });

        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }

        const isMatch = bcrypt.compareSync(password, user.passwordHash);
        if (!isMatch) {
            return res.status(400).json({ message: "Invalid credentials" });
        }

        const token = jwt.sign({ id: user.userId }, process.env.JWT_SECRET, { expiresIn: '8h' });

        res.json({ token });
    } catch (error) {
        res.status(500).json({ message: `Server error: ${error.message}` });
    }
};
