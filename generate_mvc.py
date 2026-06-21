import os

base_path = "PhanChiThongMVC"

files = {
    "Views/Shared/_Layout.cshtml": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@ViewData["Title"] - FUNewsManagement</title>
    <link rel="stylesheet" href="~/lib/bootstrap/dist/css/bootstrap.min.css" />
    <link rel="stylesheet" href="~/css/site.css" asp-append-version="true" />
</head>
<body>
    <header>
        <nav class="navbar navbar-expand-sm navbar-light bg-white border-bottom box-shadow mb-3">
            <div class="container-fluid">
                <a class="navbar-brand" asp-area="" asp-controller="Home" asp-action="Index">FUNewsManagement</a>
                <div class="navbar-collapse collapse d-sm-inline-flex justify-content-between">
                    <ul class="navbar-nav flex-grow-1">
                        <li class="nav-item"><a class="nav-link text-dark" asp-controller="Home" asp-action="Index">Home</a></li>
                        @if (Context.Session.GetInt32("Role") == 0)
                        {
                            <li class="nav-item"><a class="nav-link text-dark" asp-controller="Admin" asp-action="Index">Manage Accounts</a></li>
                            <li class="nav-item"><a class="nav-link text-dark" asp-controller="Admin" asp-action="Report">Report Statistics</a></li>
                        }
                        else if (Context.Session.GetInt32("Role") == 1)
                        {
                            <li class="nav-item"><a class="nav-link text-dark" asp-controller="Category" asp-action="Index">Categories</a></li>
                            <li class="nav-item"><a class="nav-link text-dark" asp-controller="NewsArticle" asp-action="Index">News Articles</a></li>
                            <li class="nav-item"><a class="nav-link text-dark" asp-controller="Staff" asp-action="History">My History</a></li>
                            <li class="nav-item"><a class="nav-link text-dark" asp-controller="Staff" asp-action="Profile">Profile</a></li>
                        }
                    </ul>
                    <ul class="navbar-nav">
                        @if (Context.Session.GetString("Email") != null)
                        {
                            <li class="nav-item"><span class="nav-link text-dark">Hello, @Context.Session.GetString("Email")</span></li>
                            <li class="nav-item"><a class="nav-link text-dark" asp-controller="Account" asp-action="Logout">Logout</a></li>
                        }
                        else
                        {
                            <li class="nav-item"><a class="nav-link text-dark" asp-controller="Account" asp-action="Login">Login</a></li>
                        }
                    </ul>
                </div>
            </div>
        </nav>
    </header>
    <div class="container">
        <main role="main" class="pb-3">
            @RenderBody()
        </main>
    </div>
    <script src="~/lib/jquery/dist/jquery.min.js"></script>
    <script src="~/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
""",

    "Controllers/AdminController.cs": """
using Microsoft.AspNetCore.Mvc;
using PhanChiThong_BusinessLogic.Services;
using PhanChiThong_DataAccess.Models;
using Microsoft.AspNetCore.Http;
using System.Linq;
using System;

namespace PhanChiThongMVC.Controllers
{
    public class AdminController : Controller
    {
        private readonly ISystemAccountService _accountService;
        private readonly INewsArticleService _newsArticleService;
        public AdminController(ISystemAccountService accountService, INewsArticleService newsArticleService)
        {
            _accountService = accountService;
            _newsArticleService = newsArticleService;
        }

        private bool IsAdmin() => HttpContext.Session.GetInt32("Role") == 0;

        public IActionResult Index()
        {
            if (!IsAdmin()) return RedirectToAction("Login", "Account");
            return View(_accountService.GetAll());
        }

        [HttpPost]
        public IActionResult SaveAccount(SystemAccount account)
        {
            if (!IsAdmin()) return Unauthorized();
            var existing = _accountService.GetById(account.AccountId);
            if (existing == null)
            {
                var all = _accountService.GetAll();
                account.AccountId = (short)(all.Count > 0 ? all.Max(a => a.AccountId) + 1 : 1);
                _accountService.Add(account);
            }
            else
            {
                existing.AccountName = account.AccountName;
                existing.AccountEmail = account.AccountEmail;
                existing.AccountRole = account.AccountRole;
                existing.AccountPassword = account.AccountPassword;
                _accountService.Update(existing);
            }
            return RedirectToAction("Index");
        }

        public IActionResult DeleteAccount(short id)
        {
            if (!IsAdmin()) return Unauthorized();
            var acc = _accountService.GetById(id);
            if (acc != null) _accountService.Delete(acc);
            return RedirectToAction("Index");
        }

        public IActionResult Report(DateTime? startDate, DateTime? endDate)
        {
            if (!IsAdmin()) return RedirectToAction("Login", "Account");
            var articles = _newsArticleService.GetAll();
            if (startDate.HasValue) articles = articles.Where(a => a.CreatedDate >= startDate.Value).ToList();
            if (endDate.HasValue) articles = articles.Where(a => a.CreatedDate <= endDate.Value).ToList();
            articles = articles.OrderByDescending(a => a.CreatedDate).ToList();
            ViewBag.StartDate = startDate?.ToString("yyyy-MM-dd");
            ViewBag.EndDate = endDate?.ToString("yyyy-MM-dd");
            return View(articles);
        }
    }
}
""",

    "Views/Admin/Index.cshtml": """
@model IEnumerable<PhanChiThong_DataAccess.Models.SystemAccount>
@{ ViewData["Title"] = "Manage Accounts"; }
<h2>Manage Accounts</h2>
<button class="btn btn-success mb-3" data-bs-toggle="modal" data-bs-target="#accountModal" onclick="clearForm()">Create New Account</button>
<table class="table table-bordered">
    <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Actions</th></tr></thead>
    <tbody>
        @foreach (var item in Model) {
            <tr>
                <td>@item.AccountId</td><td>@item.AccountName</td><td>@item.AccountEmail</td>
                <td>@(item.AccountRole == 1 ? "Staff" : (item.AccountRole == 2 ? "Lecturer" : "Admin"))</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editAccount(@item.AccountId, '@item.AccountName', '@item.AccountEmail', @item.AccountRole, '@item.AccountPassword')" data-bs-toggle="modal" data-bs-target="#accountModal">Edit</button>
                    <a href="/Admin/DeleteAccount/@item.AccountId" class="btn btn-danger btn-sm" onclick="return confirm('Delete this account?');">Delete</a>
                </td>
            </tr>
        }
    </tbody>
</table>

<div class="modal fade" id="accountModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <form method="post" action="/Admin/SaveAccount">
          <div class="modal-header"><h5 class="modal-title">Account</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
          <div class="modal-body">
              <input type="hidden" name="AccountId" id="AccountId" value="0" />
              <div class="mb-3"><label>Name</label><input type="text" name="AccountName" id="AccountName" class="form-control" required /></div>
              <div class="mb-3"><label>Email</label><input type="email" name="AccountEmail" id="AccountEmail" class="form-control" required /></div>
              <div class="mb-3"><label>Role</label><select name="AccountRole" id="AccountRole" class="form-control"><option value="1">Staff</option><option value="2">Lecturer</option></select></div>
              <div class="mb-3"><label>Password</label><input type="password" name="AccountPassword" id="AccountPassword" class="form-control" required /></div>
          </div>
          <div class="modal-footer"><button type="submit" class="btn btn-primary">Save</button></div>
      </form>
    </div>
  </div>
</div>
@section Scripts {
    <script>
        function clearForm() { $('#AccountId').val('0'); $('#AccountName').val(''); $('#AccountEmail').val(''); $('#AccountRole').val('1'); $('#AccountPassword').val(''); }
        function editAccount(id, name, email, role, pwd) { $('#AccountId').val(id); $('#AccountName').val(name); $('#AccountEmail').val(email); $('#AccountRole').val(role); $('#AccountPassword').val(pwd); }
    </script>
}
""",

    "Views/Admin/Report.cshtml": """
@model IEnumerable<PhanChiThong_DataAccess.Models.NewsArticle>
@{ ViewData["Title"] = "Report Statistics"; }
<h2>News Articles Report</h2>
<form method="get" action="/Admin/Report" class="row mb-4">
    <div class="col-md-4"><label>Start Date</label><input type="date" name="startDate" value="@ViewBag.StartDate" class="form-control" /></div>
    <div class="col-md-4"><label>End Date</label><input type="date" name="endDate" value="@ViewBag.EndDate" class="form-control" /></div>
    <div class="col-md-4 d-flex align-items-end"><button type="submit" class="btn btn-primary">Filter</button></div>
</form>
<table class="table table-bordered">
    <thead><tr><th>ID</th><th>Title</th><th>Created Date</th><th>Status</th></tr></thead>
    <tbody>
        @foreach (var item in Model) {
            <tr><td>@item.NewsArticleId</td><td>@item.NewsTitle</td><td>@item.CreatedDate?.ToString("yyyy-MM-dd")</td><td>@(item.NewsStatus == true ? "Active" : "Inactive")</td></tr>
        }
    </tbody>
</table>
""",

    "Controllers/CategoryController.cs": """
using Microsoft.AspNetCore.Mvc;
using PhanChiThong_BusinessLogic.Services;
using PhanChiThong_DataAccess.Models;
using Microsoft.AspNetCore.Http;
using System.Linq;

namespace PhanChiThongMVC.Controllers
{
    public class CategoryController : Controller
    {
        private readonly ICategoryService _categoryService;
        private readonly INewsArticleService _newsArticleService;
        public CategoryController(ICategoryService categoryService, INewsArticleService newsArticleService)
        {
            _categoryService = categoryService;
            _newsArticleService = newsArticleService;
        }

        private bool IsStaff() => HttpContext.Session.GetInt32("Role") == 1;

        public IActionResult Index()
        {
            if (!IsStaff()) return RedirectToAction("Login", "Account");
            return View(_categoryService.GetAll());
        }

        [HttpPost]
        public IActionResult Save(Category category)
        {
            if (!IsStaff()) return Unauthorized();
            var existing = _categoryService.GetById(category.CategoryId);
            if (existing == null)
            {
                var all = _categoryService.GetAll();
                category.CategoryId = (short)(all.Count > 0 ? all.Max(c => c.CategoryId) + 1 : 1);
                _categoryService.Add(category);
            }
            else
            {
                existing.CategoryName = category.CategoryName;
                existing.CategoryDesciption = category.CategoryDesciption;
                existing.IsActive = category.IsActive;
                _categoryService.Update(existing);
            }
            return RedirectToAction("Index");
        }

        public IActionResult Delete(short id)
        {
            if (!IsStaff()) return Unauthorized();
            var articles = _newsArticleService.GetAll().Any(a => a.CategoryId == id);
            if (articles)
            {
                TempData["Error"] = "Cannot delete category because it is already stored in a news article.";
                return RedirectToAction("Index");
            }
            var cat = _categoryService.GetById(id);
            if (cat != null) _categoryService.Delete(cat);
            return RedirectToAction("Index");
        }
    }
}
""",

    "Views/Category/Index.cshtml": """
@model IEnumerable<PhanChiThong_DataAccess.Models.Category>
@{ ViewData["Title"] = "Manage Categories"; }
<h2>Manage Categories</h2>

@if (TempData["Error"] != null)
{
    <div class="alert alert-danger">@TempData["Error"]</div>
}

<button class="btn btn-success mb-3" data-bs-toggle="modal" data-bs-target="#categoryModal" onclick="clearForm()">Create New Category</button>
<table class="table table-bordered">
    <thead><tr><th>ID</th><th>Name</th><th>Description</th><th>Status</th><th>Actions</th></tr></thead>
    <tbody>
        @foreach (var item in Model) {
            <tr>
                <td>@item.CategoryId</td><td>@item.CategoryName</td><td>@item.CategoryDesciption</td>
                <td>@(item.IsActive == true ? "Active" : "Inactive")</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editCat(@item.CategoryId, '@item.CategoryName', '@item.CategoryDesciption', @(item.IsActive==true?"true":"false"))" data-bs-toggle="modal" data-bs-target="#categoryModal">Edit</button>
                    <a href="/Category/Delete/@item.CategoryId" class="btn btn-danger btn-sm" onclick="return confirm('Delete this category?');">Delete</a>
                </td>
            </tr>
        }
    </tbody>
</table>

<div class="modal fade" id="categoryModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <form method="post" action="/Category/Save">
          <div class="modal-header"><h5 class="modal-title">Category</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
          <div class="modal-body">
              <input type="hidden" name="CategoryId" id="CategoryId" value="0" />
              <div class="mb-3"><label>Name</label><input type="text" name="CategoryName" id="CategoryName" class="form-control" required /></div>
              <div class="mb-3"><label>Description</label><input type="text" name="CategoryDesciption" id="CategoryDesciption" class="form-control" required /></div>
              <div class="mb-3">
                  <label>Status</label>
                  <select name="IsActive" id="IsActive" class="form-control">
                      <option value="true">Active</option>
                      <option value="false">Inactive</option>
                  </select>
              </div>
          </div>
          <div class="modal-footer"><button type="submit" class="btn btn-primary">Save</button></div>
      </form>
    </div>
  </div>
</div>
@section Scripts {
    <script>
        function clearForm() { $('#CategoryId').val('0'); $('#CategoryName').val(''); $('#CategoryDesciption').val(''); $('#IsActive').val('true'); }
        function editCat(id, name, desc, active) { $('#CategoryId').val(id); $('#CategoryName').val(name); $('#CategoryDesciption').val(desc); $('#IsActive').val(active ? 'true' : 'false'); }
    </script>
}
""",

    "Controllers/StaffController.cs": """
using Microsoft.AspNetCore.Mvc;
using PhanChiThong_BusinessLogic.Services;
using PhanChiThong_DataAccess.Models;
using Microsoft.AspNetCore.Http;
using System.Linq;

namespace PhanChiThongMVC.Controllers
{
    public class StaffController : Controller
    {
        private readonly ISystemAccountService _accountService;
        private readonly INewsArticleService _newsService;
        public StaffController(ISystemAccountService accountService, INewsArticleService newsService)
        {
            _accountService = accountService;
            _newsService = newsService;
        }

        private bool IsStaff() => HttpContext.Session.GetInt32("Role") == 1;

        public IActionResult Profile()
        {
            if (!IsStaff()) return RedirectToAction("Login", "Account");
            int id = HttpContext.Session.GetInt32("AccountId").Value;
            return View(_accountService.GetById((short)id));
        }

        [HttpPost]
        public IActionResult UpdateProfile(SystemAccount model)
        {
            if (!IsStaff()) return Unauthorized();
            var existing = _accountService.GetById(model.AccountId);
            if (existing != null)
            {
                existing.AccountName = model.AccountName;
                existing.AccountEmail = model.AccountEmail;
                existing.AccountPassword = model.AccountPassword;
                _accountService.Update(existing);
                ViewBag.Message = "Profile updated successfully!";
            }
            return View("Profile", existing);
        }

        public IActionResult History()
        {
            if (!IsStaff()) return RedirectToAction("Login", "Account");
            int id = HttpContext.Session.GetInt32("AccountId").Value;
            var history = _newsService.GetAll().Where(n => n.CreatedById == id).OrderByDescending(n => n.CreatedDate).ToList();
            return View(history);
        }
    }
}
""",

    "Views/Staff/Profile.cshtml": """
@model PhanChiThong_DataAccess.Models.SystemAccount
@{ ViewData["Title"] = "My Profile"; }
<h2>My Profile</h2>
@if (ViewBag.Message != null) { <div class="alert alert-success">@ViewBag.Message</div> }
<form method="post" action="/Staff/UpdateProfile">
    <input type="hidden" asp-for="AccountId" />
    <input type="hidden" asp-for="AccountRole" />
    <div class="mb-3"><label>Name</label><input asp-for="AccountName" class="form-control" required /></div>
    <div class="mb-3"><label>Email</label><input asp-for="AccountEmail" class="form-control" required /></div>
    <div class="mb-3"><label>Password</label><input asp-for="AccountPassword" type="password" class="form-control" required /></div>
    <button type="submit" class="btn btn-primary">Update Profile</button>
</form>
""",

    "Views/Staff/History.cshtml": """
@model IEnumerable<PhanChiThong_DataAccess.Models.NewsArticle>
@{ ViewData["Title"] = "My History"; }
<h2>My News History</h2>
<table class="table table-bordered">
    <thead><tr><th>ID</th><th>Title</th><th>Created Date</th><th>Status</th></tr></thead>
    <tbody>
        @foreach (var item in Model) {
            <tr><td>@item.NewsArticleId</td><td>@item.NewsTitle</td><td>@item.CreatedDate?.ToString("yyyy-MM-dd")</td><td>@(item.NewsStatus == true ? "Active" : "Inactive")</td></tr>
        }
    </tbody>
</table>
""",

    "Controllers/NewsArticleController.cs": """
using Microsoft.AspNetCore.Mvc;
using PhanChiThong_BusinessLogic.Services;
using PhanChiThong_DataAccess.Models;
using Microsoft.AspNetCore.Http;
using System.Linq;
using System;

namespace PhanChiThongMVC.Controllers
{
    public class NewsArticleController : Controller
    {
        private readonly INewsArticleService _newsService;
        private readonly ICategoryService _catService;
        public NewsArticleController(INewsArticleService newsService, ICategoryService catService)
        {
            _newsService = newsService;
            _catService = catService;
        }

        private bool IsStaff() => HttpContext.Session.GetInt32("Role") == 1;

        public IActionResult Index(string searchTitle)
        {
            if (!IsStaff()) return RedirectToAction("Login", "Account");
            ViewBag.Categories = _catService.GetAll();
            var list = _newsService.GetAll();
            if (!string.IsNullOrEmpty(searchTitle))
                list = list.Where(n => n.NewsTitle.Contains(searchTitle, StringComparison.OrdinalIgnoreCase)).ToList();
            return View(list);
        }

        [HttpPost]
        public IActionResult Save(NewsArticle article)
        {
            if (!IsStaff()) return Unauthorized();
            var existing = _newsService.GetById(article.NewsArticleId);
            if (existing == null)
            {
                article.CreatedDate = DateTime.Now;
                article.CreatedById = (short)HttpContext.Session.GetInt32("AccountId").Value;
                _newsService.Add(article);
            }
            else
            {
                existing.NewsTitle = article.NewsTitle;
                existing.Headline = article.Headline;
                existing.NewsContent = article.NewsContent;
                existing.NewsSource = article.NewsSource;
                existing.CategoryId = article.CategoryId;
                existing.NewsStatus = article.NewsStatus;
                existing.ModifiedDate = DateTime.Now;
                existing.UpdatedById = (short)HttpContext.Session.GetInt32("AccountId").Value;
                _newsService.Update(existing);
            }
            return RedirectToAction("Index");
        }

        public IActionResult Delete(string id)
        {
            if (!IsStaff()) return Unauthorized();
            var item = _newsService.GetById(id);
            if (item != null) _newsService.Delete(item);
            return RedirectToAction("Index");
        }
    }
}
""",

    "Views/NewsArticle/Index.cshtml": """
@model IEnumerable<PhanChiThong_DataAccess.Models.NewsArticle>
@{ ViewData["Title"] = "Manage News"; }
<h2>Manage News Articles</h2>

<form method="get" class="mb-3 d-flex">
    <input type="text" name="searchTitle" class="form-control me-2" placeholder="Search by title..." />
    <button type="submit" class="btn btn-primary">Search</button>
</form>

<button class="btn btn-success mb-3" data-bs-toggle="modal" data-bs-target="#newsModal" onclick="clearForm()">Create New Article</button>

<table class="table table-bordered">
    <thead><tr><th>ID</th><th>Title</th><th>Category</th><th>Status</th><th>Actions</th></tr></thead>
    <tbody>
        @foreach (var item in Model) {
            <tr>
                <td>@item.NewsArticleId</td><td>@item.NewsTitle</td><td>@(item.Category?.CategoryName)</td>
                <td>@(item.NewsStatus == true ? "Active" : "Inactive")</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editNews('@item.NewsArticleId', '@item.NewsTitle', '@item.Headline', '@item.NewsContent', '@item.NewsSource', @item.CategoryId, @(item.NewsStatus==true?"true":"false"))" data-bs-toggle="modal" data-bs-target="#newsModal">Edit</button>
                    <a href="/NewsArticle/Delete/@item.NewsArticleId" class="btn btn-danger btn-sm" onclick="return confirm('Delete this article?');">Delete</a>
                </td>
            </tr>
        }
    </tbody>
</table>

<div class="modal fade" id="newsModal" tabindex="-1">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <form method="post" action="/NewsArticle/Save">
          <div class="modal-header"><h5 class="modal-title">News Article</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
          <div class="modal-body">
              <div class="mb-3"><label>ID</label><input type="text" name="NewsArticleId" id="NewsArticleId" class="form-control" required /></div>
              <div class="mb-3"><label>Title</label><input type="text" name="NewsTitle" id="NewsTitle" class="form-control" required /></div>
              <div class="mb-3"><label>Headline</label><input type="text" name="Headline" id="Headline" class="form-control" required /></div>
              <div class="mb-3"><label>Content</label><textarea name="NewsContent" id="NewsContent" class="form-control" rows="4"></textarea></div>
              <div class="mb-3"><label>Source</label><input type="text" name="NewsSource" id="NewsSource" class="form-control" /></div>
              <div class="mb-3">
                  <label>Category</label>
                  <select name="CategoryId" id="CategoryId" class="form-control">
                      @foreach (var cat in ViewBag.Categories) { <option value="@cat.CategoryId">@cat.CategoryName</option> }
                  </select>
              </div>
              <div class="mb-3">
                  <label>Status</label>
                  <select name="NewsStatus" id="NewsStatus" class="form-control">
                      <option value="true">Active</option><option value="false">Inactive</option>
                  </select>
              </div>
          </div>
          <div class="modal-footer"><button type="submit" class="btn btn-primary">Save</button></div>
      </form>
    </div>
  </div>
</div>
@section Scripts {
    <script>
        function clearForm() { $('#NewsArticleId').val('').prop('readonly', false); $('#NewsTitle').val(''); $('#Headline').val(''); $('#NewsContent').val(''); $('#NewsSource').val(''); $('#NewsStatus').val('true'); }
        function editNews(id, title, hl, content, src, catId, active) { 
            $('#NewsArticleId').val(id).prop('readonly', true); 
            $('#NewsTitle').val(title); $('#Headline').val(hl); $('#NewsContent').val(content); $('#NewsSource').val(src); 
            $('#CategoryId').val(catId); $('#NewsStatus').val(active ? 'true' : 'false'); 
        }
    </script>
}
""",

    "Controllers/HomeController.cs": """
using Microsoft.AspNetCore.Mvc;
using PhanChiThong_BusinessLogic.Services;
using System.Linq;

namespace PhanChiThongMVC.Controllers
{
    public class HomeController : Controller
    {
        private readonly INewsArticleService _newsService;
        public HomeController(INewsArticleService newsService)
        {
            _newsService = newsService;
        }

        public IActionResult Index()
        {
            // Do not need authentication to view active news
            var activeNews = _newsService.GetAll().Where(n => n.NewsStatus == true).OrderByDescending(n => n.CreatedDate).ToList();
            return View(activeNews);
        }
    }
}
""",

    "Views/Home/Index.cshtml": """
@model IEnumerable<PhanChiThong_DataAccess.Models.NewsArticle>
@{ ViewData["Title"] = "Home Page"; }
<div class="text-center">
    <h1 class="display-4">Welcome to FUNewsManagement</h1>
    <p>Latest Active News</p>
</div>
<div class="row">
    @foreach (var item in Model) {
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">@item.NewsTitle</h5>
                    <h6 class="card-subtitle mb-2 text-muted">@item.Category?.CategoryName | @item.CreatedDate?.ToString("yyyy-MM-dd")</h6>
                    <p class="card-text">@item.Headline</p>
                    <hr />
                    <p class="card-text text-truncate">@item.NewsContent</p>
                    <p class="card-text"><small class="text-muted">Source: @item.NewsSource</small></p>
                </div>
            </div>
        </div>
    }
</div>
"""
}

for path, content in files.items():
    full_path = os.path.join(base_path, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())

print("MVC files generated successfully.")
