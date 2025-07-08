// Ground Staff Logic JavaScript for tables-gridjs.html
// This file handles the train table display and navigation

// Fetch trains data from the Flask backend
fetch("http://127.0.0.1:5000/trains")
  .then((res) => res.json())
  .then((data) => {
    // Transform data to gridjs format: [[sl_no, name, status], ...]
    const tableData = data.map((item) => [item.sl_no, item.name, item.time, item.status]);

    new gridjs.Grid({
      columns: [
        {
          name: "Sl no.",
          width: "240px",
          sort: true,
        },
        // NOTE: use size for the train name unfinsihed and finished, i.e if there's no name then it'll be unfinished
        // NOTE: use post request for using the train report id
        // NOTE: make the iit logo big and remove the side nav since the sidenav wont't be used later on
        // NOTE: station name will be from the database
        {
          name: "Train Name",
          width: "auto",
          formatter: (cell, row) => {
            const trainId = row.cells[0].data;
            const trainStatus = row.cells[2].data;
            return gridjs.html(
              `<a href="/ground-staff?name=${encodeURIComponent(
                cell
              )}&status=${trainStatus}&id=${trainId}" style="color: #011bff; text-decoration: none; font-weight: 500;">${cell}</a>`
            );
          },
          sort: true,
        },
        {
          name: "Train Time",
          width: "200px",
          formatter: (cell) => {
            // If cell is a valid date string, format it, else show as is
            if (!cell) return "";
            if (/^\d{1,2}:\d{2}(\s?[APMapm]{2})?$/.test(cell.trim())) {
              return gridjs.html(`<span style="color: #011bff; text-decoration: none; font-weight: 500;">${cell}</span>`);
            }
            // Try to parse as date
            const dateObj = new Date(cell);
            if (!isNaN(dateObj.getTime())) {
              return gridjs.html(`<span style="color: #011bff; text-decoration: none; font-weight: 500;">${dateObj.toLocaleString("en-US", {
                year: "numeric",
                month: "short",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
              })}</span>`);
            }
            // Fallback: show as is
            return gridjs.html(`<span style="color: #011bff; text-decoration: none; font-weight: 500;">${cell}</span>`);
          },
          sort: true,
        },
        {
          name: "Train Status",
          width: "280px",
          formatter: (cell, row) => {
            const trainName = row.cells[1].data;
            const trainId = row.cells[0].data;
            const isFinished = cell === "Finished";
            const bgColor = isFinished ? "#28a745" : "#dc3545";
            const hoverColor = isFinished ? "#218838" : "#c82333";

            return gridjs.html(
              `<a href="/train-report?name=${encodeURIComponent(
                trainName
              )}&status=${cell}&id=${trainId}"
                 style="background-color: ${bgColor};
                        color: white;
                        padding: 8px 16px;
                        border-radius: 6px;
                        text-decoration: none;
                        font-weight: 500;
                        display: inline-block;
                        transition: all 0.3s ease;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
                 onmouseover="this.style.backgroundColor='${hoverColor}';
                              this.style.transform='translateY(-2px)';
                              this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)';"
                 onmouseout="this.style.backgroundColor='${bgColor}';
                             this.style.transform='translateY(0px)';
                             this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                ${cell}
              </a>`
            );
          },
          sort: true,
        },
      ],
      sort: true,
      resizable: true,
      pagination: {
        enabled: true,
        limit: 10,
        summary: true,
      },
      search: {
        enabled: true,
        placeholder: "Search trains...",
      },
      fixedHeader: true,
      height: "auto",
      data: tableData,
      style: {
        table: {
          "font-size": "14px",
          "border-collapse": "collapse",
        },
        th: {
          "background-color": "#f8f9fa",
          "font-weight": "600",
          "text-align": "center",
          padding: "12px 8px",
          border: "1px solid #dee2e6",
        },
        td: {
          "text-align": "center",
          padding: "10px 8px",
          border: "1px solid #dee2e6",
        },
      },
    }).render(document.getElementById("table-fixed-header"));
  })