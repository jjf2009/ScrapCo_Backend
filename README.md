# ScrapCo Backend

A comprehensive backend solution for managing scrap material trading, built for the InternSpirit Hackathon 2025. This platform connects scrap sellers with dealers, featuring both a web-based API and a Telegram bot interface for listing scrap items.

## 🎯 Overview

ScrapCo Backend provides a complete marketplace ecosystem for buying and selling scrap materials. The platform supports two types of users (Sellers and Dealers), multiple scrap material types, and integrates with both web and Telegram platforms for maximum accessibility.

## ✨ Features

### Core Functionality
- **User Management**
  - Seller registration and authentication (Individual & Organization)
  - Dealer registration with GST and license verification
  - JWT-based authentication
  - Password hashing with bcryptjs

- **Item Management**
  - Create, read, update, and delete scrap item listings
  - Support for multiple images per item
  - Multiple material types (Aluminum, Steel, Copper, Plastic, Glass, Wood, Paper, Rubber, Textile, Iron, and more)
  - Item status tracking (Pending, Picked, Completed)
  - Dual platform listing (Website & Telegram)

- **Order & Transaction Management**
  - Order creation and tracking
  - Transaction history
  - Payment status monitoring
  - Tracking ID support for pickup and delivery

- **Rewards Shop**
  - Points-based reward system
  - Shop items with stock management
  - Category-based product organization

- **Telegram Bot Integration**
  - Easy item listing through Telegram
  - Bilingual support (English & Hindi)
  - Image upload support
  - Direct integration with the main database

## 🛠️ Technology Stack

### Backend Framework
- **Node.js** with **Express.js** - REST API server
- **Prisma ORM** - Database management and migrations
- **PostgreSQL** - Primary database

### Authentication & Security
- **jsonwebtoken** - JWT token generation and validation
- **bcryptjs** - Password hashing
- **validator** - Input validation

### Additional Libraries
- **CORS** - Cross-origin resource sharing
- **dotenv** - Environment variable management
- **multer** - File upload handling
- **@supabase/supabase-js** - Supabase integration

### Bot Framework
- **python-telegram-bot** - Telegram bot implementation

## 📊 Database Schema

### Main Models

#### User (Seller)
- Unique ID, role, and authentication credentials
- Support for both individual sellers and organizations
- Points-based reward system
- Profile management

#### Dealer
- Organization details with GST and license numbers
- Verified business credentials
- Transaction history

#### Item
- Comprehensive scrap item details
- Multi-platform support (Website & Telegram)
- Image storage (multiple images per item)
- Pickup location and time management
- Material type classification
- Status tracking

#### Transaction
- Links users, dealers, and items
- Payment status tracking
- Optional tracking ID for logistics
- Timestamp management

#### ShopItem
- Reward shop inventory
- Points-based pricing
- Stock management
- Category organization

## 🚀 Getting Started

### Prerequisites
- Node.js (v18 or higher recommended)
- PostgreSQL database
- npm or yarn package manager
- Python 3.x (for Telegram bot)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jjf2009/ScrapCo_Backend.git
   cd ScrapCo_Backend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL="postgresql://username:password@localhost:5432/scrapco_db"
   JWT_SECRET="your-secret-key-here"
   PORT=3000
   ```

4. **Run database migrations**
   ```bash
   npx prisma migrate dev
   ```

5. **Generate Prisma Client**
   ```bash
   npx prisma generate
   ```

6. **Start the development server**
   ```bash
   npm run dev
   ```

The server will start on `http://localhost:3000` (or your configured PORT)

### Telegram Bot Setup

1. **Navigate to the Bot directory**
   ```bash
   cd Bot
   ```

2. **Install Python dependencies**
   ```bash
   pip install python-telegram-bot
   ```

3. **Configure your bot token**
   Update the `TOKEN` in `main.py` with your Telegram Bot token from [@BotFather](https://t.me/botfather)

4. **Run the bot**
   ```bash
   python main.py
   ```

## 📡 API Endpoints

### Authentication

#### Register Seller
```http
POST /register
Content-Type: application/json

{
  "fullName": "John Doe",
  "phone": "1234567890",
  "email": "john@example.com",
  "password": "securepassword",
  "permAddress": "123 Main Street",
  "sellerRole": "INDIVIDUAL"
}
```

#### Login
```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

### Item Management

#### Create Item
```http
POST /create
Content-Type: application/json

{
  "seller_name": "John Doe",
  "seller_phone": "+919876543210",
  "pictures": ["https://example.com/image1.jpg"],
  "description": "Old iron rods for sale",
  "quantity": 10.5,
  "listPlat": "WEBSITE",
  "material": "IRON",
  "pickUpAddress": "123 Street, Goa",
  "pickUpTime": "2025-03-01T15:30:00Z",
  "price": 500.00
}
```

#### Get All Items
```http
GET /
```

#### Get Item by ID
```http
GET /:id
```

#### Update Item
```http
PUT /:id
Content-Type: application/json

{
  "status": "PICKED",
  "dealer_id": "dealer-uuid-here"
}
```

#### Delete Item
```http
DELETE /:id
```

### Shop Management

#### Add Shop Item
```http
POST /addItem
Content-Type: application/json

{
  "name": "Eco-Friendly Plates",
  "images": ["url1", "url2"],
  "points": 99,
  "stock": 100,
  "category": "Kitchen Items",
  "description": "Biodegradable plates",
  "company": "Green Company"
}
```

#### Get All Shop Items
```http
GET /shop/allItems
```

### Order Management

#### Create Order
```http
POST /
Content-Type: application/json

{
  "user_id": "user-uuid",
  "dealer_id": "dealer-uuid",
  "item_id": 123,
  "totalAmount": 500.00,
  "status": "PENDING"
}
```

#### Get Orders by User ID
```http
GET /:user_id
```

## 🤖 Telegram Bot Usage

The Telegram bot (`@theScrap_bot`) provides an alternative way to list scrap items:

1. Start a conversation with the bot: `/start`
2. The bot will guide you through the listing process
3. Upload an image of your scrap material
4. Provide the required details in the following format:

```
Full Name
Phone Number
Address
Material Type (e.g., Copper, Iron, Plastic)
Quantity (weight in kg)
Pickup Date and Time
Price
```

**Example:**
```
John Doe
1231231231
123 Fake Street, Goa
Copper
7.9kg
2025-03-01, 5:00 AM
₹500
```

The bot supports both English and Hindi interfaces for better accessibility.

## 📁 Project Structure

```
ScrapCo_Backend/
├── Bot/                    # Telegram bot implementation
│   ├── main.py            # Main bot file
│   └── main2-6.py         # Bot variants/versions
├── prisma/                # Database schema and migrations
│   ├── schema.prisma      # Prisma schema definition
│   └── migrations/        # Database migration files
├── src/                   # Main application source
│   ├── controllers/       # Business logic controllers
│   │   ├── sellerController.js
│   │   ├── itemController.js
│   │   ├── orderController.js
│   │   └── productController.js
│   ├── routes/           # API route definitions
│   │   ├── sellerRoutes.js
│   │   ├── itemRoutes.js
│   │   ├── orderRoutes.js
│   │   └── shopRoutes.js
│   ├── prismaClient.js   # Prisma client configuration
│   └── server.js         # Express server setup
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore rules
├── package.json         # Node.js dependencies and scripts
└── test.rest            # API testing file (REST Client)
```

## 🔐 Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL="postgresql://user:password@host:port/database"

# Authentication
JWT_SECRET="your-jwt-secret-key"

# Server
PORT=3000

# Supabase (if using)
SUPABASE_URL="your-supabase-url"
SUPABASE_KEY="your-supabase-anon-key"
```

## 🧪 Development

### Running in Development Mode
```bash
npm run dev
```

This uses Node.js with:
- `--watch` for auto-reloading
- `--env-file=.env` for environment variables
- `--experimental-strip-types` for TypeScript support
- `--experimental-sqlite` for SQLite features

### Database Management

**View database in Prisma Studio:**
```bash
npx prisma studio
```

**Create a new migration:**
```bash
npx prisma migrate dev --name migration_name
```

**Reset database:**
```bash
npx prisma migrate reset
```

## 🔒 Security Features

- Password hashing with bcryptjs (8 salt rounds)
- JWT token-based authentication (8-hour expiration)
- Environment variable protection for sensitive data
- CORS configuration for frontend access control
- Input validation for all API endpoints

## 🎨 Material Types Supported

The platform supports the following scrap materials:
- Aluminum
- Steel
- Copper
- Plastic
- Glass
- Wood
- Paper
- Rubber
- Textile
- Iron
- Other

## 📱 CORS Configuration

Currently configured to allow requests from:
- `http://localhost:5173` (Frontend development server)

To add more origins, update the `corsOptions` in `src/server.js`:

```javascript
const corsOptions = {
  origin: ["http://localhost:5173", "https://your-production-url.com"],
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true
};
```

## 🤝 Contributing

This project was developed for the InternSpirit Hackathon 2025. Contributions, issues, and feature requests are welcome!

## 📄 License

ISC License

## 👥 Authors

InternSpirit Hackathon 2025 Team

## 🙏 Acknowledgments

- Built for InternSpirit Hackathon 2025
- Telegram Bot API for bot integration
- Prisma for excellent ORM functionality
- Express.js community for the robust framework

---

For more information or support, please contact the development team.
