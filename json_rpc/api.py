{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "sale.order",
        "method": "create",
        "args": [{
            "partner_id": 1, // Set the customer to Acme Inc. (customer ID 1)
            "date_order": "2023-03-01", // Set the order date to today's date
            // Add other field values here
        }]
    },
    "id": 1
}
