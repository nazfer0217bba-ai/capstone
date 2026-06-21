# Template dataset representing typical HTML interfaces and user stories

SAMPLES = {
    "User Login & Security": {
        "user_story": """As a registered customer, I want to sign in to my account using my email address and security password so that I can access my secure profile dashboard. 
The password must be at least 8 characters long, cannot be blank, and must match complexity requirements.""",
        "html": """<form id="login-form" action="/api/login" method="POST">
  <h2>Account Sign-In</h2>
  
  <div class="form-group">
    <label for="email-address">Email Address:</label>
    <input type="email" id="email-address" name="email" placeholder="Enter your email" required />
  </div>
  
  <div class="form-group">
    <label for="password-field">Password:</label>
    <input type="password" id="password-field" name="password" placeholder="Enter your password" minlength="8" required />
  </div>
  
  <div class="form-options">
    <label>
      <input type="checkbox" id="remember-me" name="remember" /> Remember me on this device
    </label>
  </div>
  
  <button type="submit" id="btn-login" class="btn-primary">Sign In</button>
  <button type="reset" id="btn-reset">Reset Form</button>
</form>"""
    },
    
    "E-Commerce Payment Checkout": {
        "user_story": """As an active shopper, I want to enter my credit card information and billing details on the checkout page to submit my order. 
The credit card number must be exactly 16 digits, the CVV code must be between 100 and 999 (3 digits), and the billing address is required to prevent fraud.""",
        "html": """<form id="checkout-form" class="payment-form" action="/api/checkout">
  <h3>Payment & Billing Details</h3>
  
  <div class="row">
    <div class="col">
      <label for="cardholder-name">Cardholder Name:</label>
      <input type="text" id="cardholder-name" name="cardholder" placeholder="John Doe" required />
    </div>
  </div>
  
  <div class="row">
    <div class="col-8">
      <label for="cc-number">Credit Card Number:</label>
      <input type="text" id="cc-number" name="card_number" placeholder="4111 2222 3333 4444" pattern="\d{16}" required />
    </div>
    <div class="col-4">
      <label for="cc-cvv">CVV Code:</label>
      <input type="number" id="cc-cvv" name="cvv" placeholder="123" min="100" max="999" required />
    </div>
  </div>
  
  <div class="row">
    <label for="country-select">Country:</label>
    <select id="country-select" name="country" required>
      <option value="">Select your country...</option>
      <option value="US">United States</option>
      <option value="CA">Canada</option>
      <option value="UK">United Kingdom</option>
      <option value="IN">India</option>
    </select>
  </div>
  
  <div class="row">
    <label for="billing-address">Billing Address:</label>
    <textarea id="billing-address" name="address" placeholder="123 Main St, Apt 4" maxlength="200" required></textarea>
  </div>
  
  <button type="submit" id="btn-pay" class="btn-success">Pay Now</button>
</form>"""
    },
    
    "Catalog Product Search & Filters": {
        "user_story": """As a store visitor, I want to search for items by keyword query and filter by category or price range to find products quickly. 
The search keyword must not exceed 50 characters, and the minimum price input must be at least 0.""",
        "html": """<div class="search-filter-panel">
  <form id="search-filter-form" action="/catalog/search">
    <div class="field-item">
      <label for="search-query">Search Keyword:</label>
      <input type="search" id="search-query" name="q" placeholder="Search products..." maxlength="50" required />
    </div>
    
    <div class="field-item">
      <label for="category-dropdown">Category:</label>
      <select id="category-dropdown" name="category">
        <option value="all">All Categories</option>
        <option value="electronics">Electronics</option>
        <option value="apparel">Apparel & Fashion</option>
        <option value="home">Home & Kitchen</option>
      </select>
    </div>
    
    <div class="field-item price-range">
      <label for="price-min">Min Price ($):</label>
      <input type="number" id="price-min" name="min_price" min="0" placeholder="0" />
      
      <label for="price-max">Max Price ($):</label>
      <input type="number" id="price-max" name="max_price" placeholder="No Limit" />
    </div>
    
    <button type="submit" id="btn-search">Search Now</button>
  </form>
</div>"""
    }
}
