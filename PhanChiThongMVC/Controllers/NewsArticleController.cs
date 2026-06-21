using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PhanChiThong_BusinessLogic.Services;
using PhanChiThong_DataAccess.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Hosting;
using System.IO;
using System.Threading.Tasks;
using System.Linq;
using System;
using System.Collections.Generic;

namespace PhanChiThongMVC.Controllers
{
    public class NewsArticleController : Controller
    {
        private readonly INewsArticleService _newsService;
        private readonly ICategoryService _catService;
        private readonly IWebHostEnvironment _env;
        
        public NewsArticleController(INewsArticleService newsService, ICategoryService catService, IWebHostEnvironment env)
        {
            _newsService = newsService;
            _catService = catService;
            _env = env;
        }

        private bool IsStaff() => HttpContext.Session.GetInt32("Role") == 1;

        public IActionResult Index(string searchTitle)
        {
            if (!IsStaff()) return RedirectToAction("Login", "Account");
            ViewBag.Categories = _catService.GetAll();
            using var context = new FUNewsManagementContext();
            ViewBag.AllTags = context.Tags.ToList();
            
            var list = context.NewsArticles.Include(n => n.Category).Include(n => n.Tags).ToList();
            if (!string.IsNullOrEmpty(searchTitle))
                list = list.Where(n => n.NewsTitle.Contains(searchTitle, StringComparison.OrdinalIgnoreCase)).ToList();
            
            list = list.OrderBy(n => int.TryParse(n.NewsArticleId, out int val) ? val : int.MaxValue).ToList();
            
            return View(list);
        }

        [HttpPost]
        public async Task<IActionResult> Save(NewsArticle article, List<int> TagIds, IFormFile? ImageFile, bool IsUpdate)
        {
            if (!IsStaff()) return Unauthorized();
            
            // Xử lý Upload Ảnh
            if (ImageFile != null && ImageFile.Length > 0)
            {
                var uploadsFolder = Path.Combine(_env.WebRootPath, "images", "news");
                if (!Directory.Exists(uploadsFolder)) Directory.CreateDirectory(uploadsFolder);
                
                var uniqueFileName = Guid.NewGuid().ToString() + "_" + ImageFile.FileName;
                var filePath = Path.Combine(uploadsFolder, uniqueFileName);
                
                using (var stream = new FileStream(filePath, FileMode.Create))
                {
                    await ImageFile.CopyToAsync(stream);
                }
                
                article.ImageUrl = "/images/news/" + uniqueFileName;
            }

            using var context = new FUNewsManagementContext();
            var existing = context.NewsArticles.Include(n => n.Tags).FirstOrDefault(n => n.NewsArticleId == article.NewsArticleId);
            
            var selectedTags = context.Tags.Where(t => TagIds.Contains(t.TagId)).ToList();

            if (!IsUpdate)
            {
                if (existing != null)
                {
                    TempData["ErrorMessage"] = $"Article ID '{article.NewsArticleId}' already exists. Please choose another ID.";
                    return RedirectToAction("Index");
                }
                
                article.CreatedDate = DateTime.Now;
                article.CreatedById = (short)HttpContext.Session.GetInt32("AccountId").Value;
                article.Tags = selectedTags;
                context.NewsArticles.Add(article);
            }
            else
            {
                existing.NewsTitle = article.NewsTitle;
                existing.Headline = article.Headline;
                existing.NewsContent = article.NewsContent;
                existing.NewsSource = article.NewsSource;
                existing.CategoryId = article.CategoryId;
                existing.NewsStatus = article.NewsStatus;
                existing.ImageUrl = article.ImageUrl;
                existing.ModifiedDate = DateTime.Now;
                existing.UpdatedById = (short)HttpContext.Session.GetInt32("AccountId").Value;
                
                existing.Tags.Clear();
                foreach(var t in selectedTags) existing.Tags.Add(t);
                
                context.NewsArticles.Update(existing);
            }
            context.SaveChanges();
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