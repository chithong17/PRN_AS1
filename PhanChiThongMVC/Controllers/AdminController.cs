using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
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
                // Identity column will handle ID generation
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

        public IActionResult ExportReport(DateTime? startDate, DateTime? endDate)
        {
            if (!IsAdmin()) return Unauthorized();

            var articles = _newsArticleService.GetAll();
            if (startDate.HasValue) articles = articles.Where(a => a.CreatedDate >= startDate.Value).ToList();
            if (endDate.HasValue) articles = articles.Where(a => a.CreatedDate <= endDate.Value).ToList();
            articles = articles.OrderByDescending(a => a.CreatedDate).ToList();

            var builder = new System.Text.StringBuilder();
            builder.AppendLine("ID,Title,Created Date,Status,Views");

            foreach (var item in articles)
            {
                var id = item.NewsArticleId;
                // Escape commas in title by wrapping in quotes
                var title = item.NewsTitle != null ? $"\"{item.NewsTitle.Replace("\"", "\"\"")}\"" : "";
                var date = item.CreatedDate?.ToString("yyyy-MM-dd HH:mm");
                var status = item.NewsStatus == true ? "Active" : "Inactive";
                var views = item.ViewCount ?? 0;
                
                builder.AppendLine($"{id},{title},{date},{status},{views}");
            }

            return File(System.Text.Encoding.UTF8.GetBytes(builder.ToString()), "text/csv", "NewsReport.csv");
        }

        public IActionResult Dashboard()
        {
            if (!IsAdmin()) return Unauthorized();

            using var context = new FUNewsManagementContext();
            
            // 1. Calculate KPIs
            var totalArticles = context.NewsArticles.Count();
            var totalViews = context.NewsArticles.Sum(a => a.ViewCount) ?? 0;
            var totalStaffs = context.SystemAccounts.Count(a => a.AccountRole == 1);
            var totalCategories = context.Categories.Count();

            ViewBag.TotalArticles = totalArticles;
            ViewBag.TotalViews = totalViews;
            ViewBag.TotalStaffs = totalStaffs;
            ViewBag.TotalCategories = totalCategories;

            // 2. Pie Chart: Views by Category
            var viewsByCategory = context.NewsArticles
                .Include(n => n.Category)
                .Where(n => n.Category != null)
                .AsEnumerable()
                .GroupBy(n => n.Category.CategoryName)
                .Select(g => new { 
                    Category = g.Key, 
                    Views = g.Sum(n => n.ViewCount ?? 0) 
                }).ToList();
            
            ViewBag.PieLabels = System.Text.Json.JsonSerializer.Serialize(viewsByCategory.Select(x => x.Category));
            ViewBag.PieData = System.Text.Json.JsonSerializer.Serialize(viewsByCategory.Select(x => x.Views));

            // 3. Bar Chart: Articles by Staff
            var articlesByStaff = context.NewsArticles
                .Include(n => n.CreatedBy)
                .AsEnumerable()
                .GroupBy(n => n.CreatedBy?.AccountName ?? "Unknown")
                .Select(g => new { 
                    Staff = g.Key, 
                    Count = g.Count() 
                }).ToList();

            ViewBag.BarLabels = System.Text.Json.JsonSerializer.Serialize(articlesByStaff.Select(x => x.Staff));
            ViewBag.BarData = System.Text.Json.JsonSerializer.Serialize(articlesByStaff.Select(x => x.Count));

            return View();
        }
    }
}