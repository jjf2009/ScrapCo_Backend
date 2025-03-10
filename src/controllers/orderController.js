import prisma from "../prismaClient.js";

// Create an order
export const createOrder = async (req, res) => {
  try {
    const { user_id, dealer_id, item_id, totalAmount, status } = req.body;

    if (!user_id || !dealer_id || !item_id || !totalAmount) {
      return res.status(400).json({ message: "All fields are required" });
    }

    const newOrder = await prisma.order.create({
      data: {
        user_id,
        dealer_id,
        item_id,
        totalAmount,
        status: status || "PENDING", // Default status
      },
    });

    res.status(201).json(newOrder);
  } catch (error) {
    console.error("Error creating order", error);
    res.status(500).json({ message: "Failed to create order", error: error.message });
  }
};

// Get all orders by user email
export const getOrdersByUserId = async (req, res) => {
  try {
    const { user_id } = req.params;
    const orders = await prisma.order.findMany({
      where: { user_id },
      orderBy: { createdAt: "desc" },
      include: {
        item: true,  // Include item details
        dealer: true, // Include dealer details
      },
    });

    if (!orders.length) {
      return res.status(404).json({ message: "No orders found for this user" });
    }

    res.status(200).json(orders);
  } catch (error) {
    console.error("Error fetching orders", error);
    res.status(500).json({ message: "Failed to fetch orders", error: error.message });
  }
};
