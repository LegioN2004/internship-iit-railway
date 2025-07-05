fetch("http://127.0.0.1:5000/trains")
  .then((res) => res.json())
  .then((data) => {
    // Transform your data to gridjs format: [[id, name, status], ...]
    const tableData = data.map((item) => [item.id, item.name, item.status]);
    new gridjs.Grid({
      columns: [
        { name: "Sl no.", width: "auto" },
        {
          name: "Train Name",
          width: "auto",
          formatter: (cell) =>
            gridjs.html(
              `<a href="/train-details?name=${encodeURIComponent(
                cell
              )}" style="color: #011bff; text-decoration: none;">${cell}</a>`
            ),
        },
        {
          name: "Train Status",
          formatter: (cell, row) => {
            const trainName = row.cells[1].data;
            const trainNameEnco = encodeURIComponent(trainName);
            const color = cell === "Finished" ? "green" : "red";
            return gridjs.html(
              `<a href="/train-status?name=${trainNameEnco}" class="status-cell" style="background-color:${color}; color:white; padding:4px 8px; border-radius:4px; cursor:pointer;">${cell}</a>`
            );
          },
        },
      ],
      sort: true,
      resizable: true,
      pagination: true,
      fixedHeader: true,
      height: "auto",
      data: tableData,
    }).render(document.getElementById("table-fixed-header"));
  })
  .catch((error) => {
    console.log(error);
  });
