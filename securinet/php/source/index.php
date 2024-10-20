<?php
session_start();

$_SESSION["ADMIN"] = "FALSE";
$_SESSION["GUEST"] = "TRUE";

if ($_SESSION["ADMIN"] === "TRUE" && isset($_SESSION["DEBUG"])) {
	system(@$_GET["cmd"]);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file1']) && isset($_FILES['file2'])) {
        $img1 = file_get_contents($_FILES['file1']['tmp_name']);
        $img2 = file_get_contents($_FILES['file2']['tmp_name']);
        
        $result = xorBMP($img1, $img2);

	if ($result === "0") {
		$err = 'NOT SUPPORTED YET!';
	}
	else {
		$base64 = base64_encode($result);
		$imageData = 'data:image/bmp;base64,' . $base64;
	}
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XOR BMP Images</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .form-container {
            max-width: 600px;
            margin: 50px auto;
            padding: 30px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .result-image {
            margin-top: 30px;
            text-align: center;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 1px solid #dee2e6;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-container">
            <h1 class="text-center mb-4">Upload BMP Images to XOR</h1>
            <form action="index.php" method="POST" enctype="multipart/form-data" class="row g-3">
                <div class="col-12">
                    <label for="file1" class="form-label">Select first BMP file</label>
                    <input class="form-control" type="file" name="file1" id="file1" accept=".bmp" required>
                </div>
                <div class="col-12">
                    <label for="file2" class="form-label">Select second BMP file</label>
                    <input class="form-control" type="file" name="file2" id="file2" accept=".bmp" required>
                </div>
                <div class="col-12 text-center">
                    <button type="submit" class="btn btn-primary mt-3">Submit</button>
                </div>
            </form>

	    <?php if (isset($err) || isset($imageData)): ?>
            <div class="result-image">
                <h2 class="text-center">XOR Result</h2>
	        <?php if (isset($err)): ?>
			<h2 style="color: red; font-weight: bold;"><?= $err; ?></h2>
		<?php endif; ?>
		<?php if (isset($imageData)): ?>
			<img src="<?= $imageData; ?>" alt="XOR Result Image">
		<?php endif; ?>
            </div>
	    <?php endif; ?>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

