// Ground Staff Logic JavaScript for tables-gridjs.html
// This file handles the train table display and navigation

// Fetch trains data from the Flask backend
fetch("http://127.0.0.1:5000/trains")
  .then((res) => res.json())
  .then((data) => {
    // Transform data to gridjs format: [[sl_no, name, status], ...]
    const tableData = data.map((item) => [item.sl_no, item.name, item.status]);

    new gridjs.Grid({
      columns: [
        {
          name: "Sl no.",
          width: "240px",
          sort: true,
        },
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
          name: "Train Status",
          width: "280px",
          formatter: (cell, row) => {
            const trainName = row.cells[1].data;
            const trainId = row.cells[0].data;
            const isFinished = cell === "Finished";
            const bgColor = isFinished ? "#28a745" : "#dc3545";
            const hoverColor = isFinished ? "#218838" : "#c82333";

            return gridjs.html(
              `<a href="/ground-staff?name=${encodeURIComponent(
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
  .catch((error) => {
    console.error("Error fetching trains data:", error);

    // Fallback data if API is not available
    const fallbackData = [
      ["1", "Golden Express", "Finished"],
      ["2", "Silver Arrow", "Unfinished"],
      ["3", "Blue Mountain", "Finished"],
      ["4", "Red Falcon", "Unfinished"],
      ["5", "Eastern Star", "Finished"],
    ];

    new gridjs.Grid({
      columns: [
        { name: "Sl no.", width: "240px" },
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
              `<a href="/ground-staff?name=${encodeURIComponent(
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
        },
      ],
      data: fallbackData,
      pagination: { limit: 5 },
    }).render(document.getElementById("table-fixed-header"));
  });
