<?php
session_start();
require 'db.php';
$error='';
if($_SERVER['REQUEST_METHOD']==='POST'){
  $username=trim($_POST['username'] ?? '');
  $password=trim($_POST['password'] ?? '');
  $stmt=$conn->prepare('SELECT id,username,password,role FROM users WHERE username=? LIMIT 1');
  $stmt->bind_param('s',$username);
  $stmt->execute();
  $res=$stmt->get_result();
  if($u=$res->fetch_assoc()){
    if($password===$u['password']){
      $_SESSION['user']=['id'=>$u['id'],'username'=>$u['username'],'role'=>$u['role']];
      if(!isset($_SESSION['cart'])) $_SESSION['cart']=[];
      header('Location:index.php'); exit;
    }else $error='Sai tên đăng nhập hoặc mật khẩu.';
  }else $error='Tài khoản không tồn tại.';
}
include 'header.php';
?>
<div class="card" style="max-width:480px;margin:20px auto">
  <h3>Đăng nhập</h3>
  <?php if($error): ?><div style="color:#a94442;background:#f2dede;padding:10px;border-radius:4px"><?php echo $error; ?></div><?php endif; ?>
  <form method="post">
    <div style="margin:10px 0"><input name="username" placeholder="Tên đăng nhập" required style="width:100%;padding:8px"></div>
    <div style="margin:10px 0"><input type="password" name="password" placeholder="Mật khẩu" required style="width:100%;padding:8px"></div>
    <div><button>Đăng nhập</button> <a href="register.php" style="margin-left:10px">Đăng ký</a></div>
  </form>
</div>
<?php include 'footer.php'; ?>