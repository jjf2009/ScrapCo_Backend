import prisma from "../prismaClient.js";

// Create a new product
export const createProduct = async (req, res) => {
  try {
    const { seller_id, images, name, description, price, stock, category } = req.body;

    if (!seller_id || !images.length || !name || !description || !price || !stock || !category) {
      return res.status(400).json({ message: "All fields are required" });
    }

    const product = await prisma.product.create({
      data: {
        seller_id,
        images,
        name,
        description,
        price: parseFloat(price),
        stock: parseInt(stock),
        category
      }
    });

    res.status(201).json(product);
  } catch (error) {
    res.status(500).json({ message: "Failed to create product", error: error.message });
  }
};

// Get all products
export const getAllProducts = async (req, res) => {
  try {
    const products = await prisma.product.findMany();
    res.json(products);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch products", error: error.message });
  }
};

// Get a single product by ID
export const getProductById = async (req, res) => {
  try {
    const { id } = req.params;
    const product = await prisma.product.findUnique({ where: { productId: id } });

    if (!product) return res.status(404).json({ message: "Product not found" });

    res.json(product);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch product", error: error.message });
  }
};

// Update a product
export const updateProduct = async (req, res) => {
  try {
    const { id } = req.params;
    const { images, name, description, price, stock, category } = req.body;

    const updatedProduct = await prisma.product.update({
      where: { productId: id },
      data: {
        images,
        name,
        description,
        price: parseFloat(price),
        stock: parseInt(stock),
        category
      }
    });

    res.json(updatedProduct);
  } catch (error) {
    res.status(500).json({ message: "Failed to update product", error: error.message });
  }
};

// Delete a product
export const deleteProduct = async (req, res) => {
  try {
    const { id } = req.params;
    await prisma.product.delete({ where: { productId: id } });

    res.json({ message: "Product deleted successfully" });
  } catch (error) {
    res.status(500).json({ message: "Failed to delete product", error: error.message });
  }
};
