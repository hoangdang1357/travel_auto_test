<?php
// Simple handler to collect search params (front-end demo only)
$destination = isset($_GET['destination']) ? htmlspecialchars($_GET['destination']) : '';
$checkin = isset($_GET['checkin']) ? htmlspecialchars($_GET['checkin']) : '';
$checkout = isset($_GET['checkout']) ? htmlspecialchars($_GET['checkout']) : '';
$adults = isset($_GET['adults']) ? intval($_GET['adults']) : 2;
$children = isset($_GET['children']) ? intval($_GET['children']) : 0;
$rooms = isset($_GET['rooms']) ? intval($_GET['rooms']) : 1;
?>
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Trang đặt phòng — Demo PHP UI</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    :root{
      --brand:#003b95;
      --brand-2:#00224f;
      --accent:#febb02;
    }
    body{background:#f7f7f9;}
    .navbar{background:var(--brand);}
    .navbar .navbar-brand, .navbar .nav-link, .navbar .btn{color:#fff;}
    .hero{
      background:var(--brand);
      color:#fff;
      padding:48px 0 72px;
      position:relative;
    }
    .search-card{
      position:relative;
      margin-top:-36px;
      border-radius:16px;
      box-shadow:0 10px 30px rgba(0,0,0,.12);
    }
    .search-card .form-control, .search-card .form-select{
      height:56px;
      border-radius:12px;
    }
    .search-card .btn-search{
      height:56px;
      border-radius:12px;
      background:var(--accent);
      color:#222;
      font-weight:600;
      letter-spacing:.2px;
    }
    .section-title{
      font-weight:700;
      margin-bottom:12px;
    }
    .card{
      border:0;
      border-radius:18px;
      overflow:hidden;
      box-shadow:0 6px 20px rgba(0,0,0,.08);
    }
    .card-img-top{
      height:180px;
      object-fit:cover;
    }
    .badge-soft{
      background:rgba(254,187,2,.18);
      color:#7a5600;
      border:1px dashed rgba(254,187,2,.6);
    }
    .footer{
      background:#0c1b3f;
      color:#cfd6e6;
      padding:40px 0;
    }
    .pill{
      background:#fff;
      border-radius:999px;
      padding:8px 14px;
      font-size:.9rem;
      border:1px solid #e6e7ec;
    }
  </style>
</head>
<body>
  <!-- Top Nav -->
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container">
      <a class="navbar-brand fw-bold" href="#"><i class="bi bi-building"></i> Booking UI</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="nav">
        <ul class="navbar-nav ms-auto align-items-lg-center gap-lg-3">
          <li class="nav-item"><a class="nav-link" href="#">Lưu trú</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Chuyến bay</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Thuê xe</a></li>
          <li class="nav-item"><a class="nav-link" href="#"><i class="bi bi-question-circle"></i> Trợ giúp</a></li>
          <li class="nav-item ms-lg-2"><a class="btn btn-outline-light btn-sm" href="#">Đăng ký</a></li>
          <li class="nav-item"><a class="btn btn-light btn-sm ms-lg-2" href="#">Đăng nhập</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <section class="hero">
    <div class="container">
      <h1 class="display-6 fw-bold mb-2">Tìm chỗ nghỉ tiếp theo</h1>
      <p class="mb-0">Săn ưu đãi khách sạn, nhà và nhiều hơn nữa.</p>
    </div>
  </section>

  <!-- Search Card -->
  <div class="container">
    <div class="card search-card p-3 p-md-4">
      <form class="row g-2 g-md-3 align-items-center" method="GET" action="index.php">
        <div class="col-12 col-lg-4">
          <label class="form-label small text-muted mb-1">Bạn muốn đến đâu?</label>
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-geo-alt"></i></span>
            <input type="text" class="form-control" name="destination" placeholder="Thành phố, điểm đến..." value="<?php echo $destination; ?>" required>
          </div>
        </div>
        <div class="col-6 col-lg-2">
          <label class="form-label small text-muted mb-1">Ngày nhận phòng</label>
          <input type="date" class="form-control" name="checkin" value="<?php echo $checkin; ?>" required>
        </div>
        <div class="col-6 col-lg-2">
          <label class="form-label small text-muted mb-1">Ngày trả phòng</label>
          <input type="date" class="form-control" name="checkout" value="<?php echo $checkout; ?>" required>
        </div>
        <div class="col-12 col-lg-3">
          <label class="form-label small text-muted mb-1">Khách & Phòng</label>
          <div class="d-flex gap-2">
            <select class="form-select" name="adults">
              <?php for($i=1;$i<=9;$i++): ?>
              <option value="<?php echo $i; ?>" <?php echo $i==$adults?'selected':''; ?>><?php echo $i; ?> người lớn</option>
              <?php endfor; ?>
            </select>
            <select class="form-select" name="children">
              <?php for($i=0;$i<=9;$i++): ?>
              <option value="<?php echo $i; ?>" <?php echo $i==$children?'selected':''; ?>><?php echo $i; ?> trẻ em</option>
              <?php endfor; ?>
            </select>
            <select class="form-select" name="rooms">
              <?php for($i=1;$i<=9;$i++): ?>
              <option value="<?php echo $i; ?>" <?php echo $i==$rooms?'selected':''; ?>><?php echo $i; ?> phòng</option>
              <?php endfor; ?>
            </select>
          </div>
        </div>
        <div class="col-12 col-lg-1 d-grid">
          <button class="btn btn-search" type="submit"><i class="bi bi-search"></i> Tìm</button>
        </div>
      </form>
      <div class="mt-3 d-flex align-items-center gap-2">
        <input class="form-check-input" type="checkbox" id="addFlight">
        <label class="form-check-label small text-muted" for="addFlight">Thêm chuyến bay vào tìm kiếm của tôi</label>
      </div>
    </div>
  </div>

  <?php if(!empty($destination)): ?>
  <!-- Mini search summary (fake results header) -->
  <div class="container mt-4">
    <div class="alert alert-light border d-flex align-items-center justify-content-between">
      <div>
        <span class="badge badge-soft me-2">Tìm kiếm</span>
        <strong><?php echo $destination; ?></strong> •
        từ <strong><?php echo $checkin; ?></strong> đến <strong><?php echo $checkout; ?></strong> •
        <?php echo $adults; ?> NL, <?php echo $children; ?> TE • <?php echo $rooms; ?> phòng
      </div>
      <a href="index.php" class="btn btn-sm btn-outline-secondary">Xoá</a>
    </div>
  </div>
  <?php endif; ?>

  <!-- Deals Carousel -->
  <div class="container my-5">
    <div class="d-flex align-items-end justify-content-between mb-2">
      <h2 class="section-title">Ưu đãi</h2>
      <a href="#" class="pill text-decoration-none">Xem tất cả</a>
    </div>
    <div id="deals" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <?php
        $deals = [
          ["title"=>"Nghỉ dưỡng trong ngôi nhà mơ ước","desc"=>"Với giá ưu đãi, cho chuyến đi thêm thú vị","img"=>"https://picsum.photos/seed/home/1200/420"],
          ["title"=>"Vui là chính, không cần đợi","desc"=>"Tận hưởng thêm chức năng vàng cuối mùa với giảm giá tới 15%","img"=>"https://picsum.photos/seed/sun/1200/420"],
          ["title"=>"Ưu đãi cuối năm","desc"=>"Cơ hội hiếm có cho chuyến đi sắp tới","img"=>"https://picsum.photos/seed/winter/1200/420"],
        ];
        foreach($deals as $i=>$d):
        ?>
        <div class="carousel-item <?php echo $i===0?'active':''; ?>">
          <div class="card overflow-hidden">
            <img class="d-block w-100" src="<?php echo $d['img']; ?>" alt="deal">
            <div class="card-img-overlay bg-dark bg-opacity-25 d-flex flex-column justify-content-end">
              <div class="p-3 p-md-4 text-white">
                <span class="badge bg-warning text-dark mb-2">Ưu đãi cuối năm</span>
                <h5 class="fw-bold"><?php echo $d['title']; ?></h5>
                <p class="mb-3"><?php echo $d['desc']; ?></p>
                <a href="#" class="btn btn-light btn-sm">Tìm ưu đãi</a>
              </div>
            </div>
          </div>
        </div>
        <?php endforeach; ?>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#deals" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#deals" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>

  <!-- Explore VN -->
  <div class="container my-4">
    <h2 class="section-title">Khám phá Việt Nam</h2>
    <p class="text-muted">Các điểm đến phổ biến có nhiều điều chờ đón bạn</p>
    <div class="row g-3">
      <?php
      $cities = [
        ["TP. Hồ Chí Minh", "https://picsum.photos/seed/hcm/800/600"],
        ["Đà Nẵng", "https://picsum.photos/seed/danang/800/600"],
        ["Vũng Tàu", "https://picsum.photos/seed/vungtau/800/600"],
        ["Hà Nội", "https://picsum.photos/seed/hanoi/800/600"],
        ["Đà Lạt", "https://picsum.photos/seed/dalat/800/600"],
        ["Nha Trang", "https://picsum.photos/seed/nhatrang/800/600"]
      ];
      foreach($cities as $c):
      ?>
      <div class="col-6 col-md-4 col-lg-2">
        <div class="card">
          <img src="<?php echo $c[1]; ?>" class="card-img-top" alt="<?php echo $c[0]; ?>">
          <div class="card-body">
            <h6 class="card-title mb-0"><?php echo $c[0]; ?></h6>
            <small class="text-muted">Hàng nghìn chỗ nghỉ</small>
          </div>
        </div>
      </div>
      <?php endforeach; ?>
    </div>
  </div>

  <!-- By Category -->
  <div class="container my-5">
    <h2 class="section-title">Tìm theo loại chỗ nghỉ</h2>
    <div class="row g-3">
      <?php
      $types = [
        ["Khách sạn","https://picsum.photos/seed/hotel/800/600"],
        ["Căn hộ","https://picsum.photos/seed/apartment/800/600"],
        ["Biệt thự","https://picsum.photos/seed/villa/800/600"],
        ["Resort","https://picsum.photos/seed/resort/800/600"],
        ["Nhà nghỉ B&B","https://picsum.photos/seed/bb/800/600"],
        ["Nhà nghỉ dưỡng","https://picsum.photos/seed/house/800/600"],
      ];
      foreach($types as $t):
      ?>
      <div<a href="#" class="text-decoration-none text-light me-3">Điều khoản</a>
          <a href="#" class="text-decoration-none text-light me-3">Bảo mật</a>
          <a href="#" class="text-decoration-none text-light">Liên hệ</a>
        </div>
      </div>
    </div>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html> class="col-12 col-sm-6 col-lg-4">
        <div class="card flex-row align-items-center">
          <img src="<?php echo $t[1]; ?>" class="card-img-top" style="width:40%; height:140px; object-fit:cover;" alt="<?php echo $t[0]; ?>">
          <div class="card-body">
            <h5 class="card-title mb-1"><?php echo $t[0]; ?></h5>
            <p class="card-text text-muted mb-2">Hàng ngàn lựa chọn cho bạn</p>
            <a href="#" class="btn btn-outline-primary btn-sm">Khám phá</a>
          </div>
        </div>
      </div>
      <?php endforeach; ?>
    </div>
  </div>

  <footer class="footer mt-5">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <h5 class="text-white">Booking UI</h5>
          <p class="mb-0">Demo giao diện đặt phòng bằng PHP + Bootstrap.</p>
        </div>
        <div class="col-md-6 text-md-end mt-3 mt-md-0">
          
