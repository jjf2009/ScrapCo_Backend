import { createClient } from "@supabase/supabase-js";
import dotenv from "dotenv";
dotenv.config();

// Initialize Supabase Client
const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.VITE_SUPABASE_ANON_KEY);

// Upload Image
export const uploadImage = async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ message: "No file uploaded" });

    const file = req.file;
    const fileName = `${Date.now()}_${file.originalname}`;

    // Upload file to Supabase Storage
    const { data, error } = await supabase.storage
      .from("uploads") // Bucket name
      .upload(fileName, file.buffer, { contentType: file.mimetype });

    if (error) throw error;

    // Get public URL
    const imageUrl = `${process.env.SUPABASE_URL}/storage/v1/object/public/uploads/${fileName}`;

    res.json({ imageUrl });

  } catch (error) {
    console.error("Upload error:", error);
    res.status(500).json({ message: "Failed to upload image", error: error.message });
  }
};
