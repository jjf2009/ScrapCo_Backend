import prisma from "../prismaClient.js";

// Create a new item
export const createItem = async (req, res) => {
  try {
    const { user_id, description, quantity, material, pickUpAddress, pickUpTime, seller_name, seller_phone, listPlat, price} = req.body;

    if ( !description || !quantity || !material || !pickUpAddress || !pickUpTime) {
      return res.status(400).json({ message: "All fields are required" });
    }
    const item = await prisma.item.create({
      data: {
        seller_name,
        seller_phone,
        description,
        quantity,
        material,
        pickUpAddress,
        pickUpTime,
        listPlat,
        price,
        // pictures: pictures || [],  // Save image URLs here
        user_id: user_id  // ✅ Establish relation if user_id exists
      },
    });
    

    res.status(201).json(item);
  } catch (error) {
    res.status(500).json({ message: "Failed to create item", error: error.message });
  }
};

// Get all items
export const getAllItems = async (req, res) => {
  try {
    const items = await prisma.item.findMany();
    res.json(items);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch items", error: error.message });
  }
};

// Get a single item by ID
export const getItemById = async (req, res) => {
  try {
    const { id } = req.params;
    const item = await prisma.item.findUnique({ where: { itemId: id } });

    if (!item) return res.status(404).json({ message: "Item not found" });

    res.json(item);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch item", error: error.message });
  }
};

// Update an item
export const updateItem = async (req, res) => {
  try {
    const { id } = req.params;
    const { pictures, description, quantity, material, pickUpAddress, pickUpTime, status, dealer_id } = req.body;

    const updatedItem = await prisma.item.update({
      where: { itemId: id },
      data: {
        pictures,
        description,
        quantity,
        material,
        pickUpAddress,
        pickUpTime: new Date(pickUpTime),
        status,
        dealer_id
      }
    });

    res.json(updatedItem);
  } catch (error) {
    res.status(500).json({ message: "Failed to update item", error: error.message });
  }
};

// Delete an item
export const deleteItem = async (req, res) => {
  try {
    const { id } = req.params;
    await prisma.item.delete({ where: { itemId: id } });

    res.json({ message: "Item deleted successfully" });
  } catch (error) {
    res.status(500).json({ message: "Failed to delete item", error: error.message });
  }
};
