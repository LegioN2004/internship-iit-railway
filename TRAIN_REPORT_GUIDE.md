# Train Report System - Quick Start Guide

## 📁 File Structure

```
greeva/
├── templates/pages/
│   ├── tables-gridjs.html          # Main train list page
│   ├── train-report.html           # Detailed train report page
│   └── train-status.html           # Train status page (no sidebar)
├── static/js/components/
│   ├── train-grid.js               # Main train table logic
│   ├── table-gridjs.js             # Original table logic (fallback)
│   └── train-report.js             # Report page table logic
├── pages/
│   ├── views.py                    # Django backend views
│   └── urls.py                     # URL routing
└── python-backend/
    └── app.py                      # Flask API server
```

## 🚀 How It Works

### 1. **Main Train List** (`tables-gridjs.html`)
- Displays all trains in a grid
- Fetches data from Flask API (`http://127.0.0.1:5000/trains`)
- **Status buttons** (Finished/Unfinished) redirect to train-report page
- Uses `train-grid.js` for logic

### 2. **Train Report Page** (`train-report.html`)
- Shows detailed inspection report for a specific train
- Gets train info via URL parameters: `/train-report?name=TrainName&status=Finished`
- Displays summary statistics and detailed door information
- Print-friendly styling
- Back button to return to train list

### 3. **Backend Integration**
- **Django Views**: Handle train report requests with dynamic data
- **Flask API**: Provides train data via REST endpoints
- **URL Routing**: Clean URLs for navigation

## 🔄 Data Flow

1. **User clicks train status** in main table
2. **JavaScript** redirects to: `/train-report?name=TrainName&status=Status`
3. **Django view** processes request and renders template with data
4. **Report page** displays comprehensive train inspection details

## 🎯 Key Features

### **Train List Page**
- ✅ Real-time date display
- ✅ Search and pagination
- ✅ Sortable columns
- ✅ Status-based color coding
- ✅ Direct navigation to reports

### **Train Report Page**
- ✅ Professional report layout
- ✅ Summary statistics cards
- ✅ Detailed door information table
- ✅ Print functionality
- ✅ Status badges
- ✅ Navigation breadcrumbs

### **Backend**
- ✅ Django view for report rendering
- ✅ Flask API for train data
- ✅ Dynamic data based on URL parameters
- ✅ Clean URL routing

## 📋 URL Endpoints

| Endpoint | Purpose | Parameters |
|----------|---------|------------|
| `/tables-gridjs/` | Main train list | None |
| `/train-report/` | Train report | `name`, `status`, `id` |
| `/trains` (API) | Get trains data | None |
| `/train-report-data` (API) | Get report data | `name`, `status`, `id` |

## 🛠️ Customization

### **Adding New Columns**
Edit `train-grid.js` columns array:
```javascript
columns: [
  { name: "Sl no.", width: "100px" },
  { name: "Train Name", width: "auto" },
  { name: "Train Status", width: "150px" },
  { name: "New Column", width: "120px" } // Add here
]
```

### **Modifying Report Data**
Edit `views.py` in the `train_report_view` function:
```python
train_data = {
    'train_name': train_name,
    'custom_field': 'Your Value',  # Add custom fields
    # ... existing fields
}
```

### **Styling Changes**
- **Train List**: Edit styles in `tables-gridjs.html`
- **Train Report**: Edit styles in `train-report.html`
- **Grid Styling**: Modify `train-grid.js` style object

## 🔧 Running the System

1. **Start Flask API**:
   ```bash
   cd greeva/python-backend/
   python app.py
   ```

2. **Start Django Server**:
   ```bash
   cd greeva/
   python manage.py runserver
   ```

3. **Access Application**:
   - Main page: `http://localhost:8000/tables-gridjs/`
   - Direct report: `http://localhost:8000/train-report/?name=TestTrain&status=Finished`

## 🎨 Status Button Behavior

When you click a status button (Finished/Unfinished):
1. Opens train report in **new tab**
2. Passes train name and status as URL parameters
3. Django backend processes the request
4. Displays formatted report with real-time data

## 📝 Notes

- The system is designed to be **print-friendly**
- All navigation preserves the current context
- The Flask API provides fallback data if needed
- Bootstrap styling ensures responsive design
- Error handling for missing trains/data

This system provides a complete train inspection workflow from listing to detailed reporting! 🚂
