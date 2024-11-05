using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.IdentityModel.Tokens;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenQA.Selenium;
using OpenQA.Selenium.Support.UI;
using OpenQA.Selenium.BiDi.Modules.Log;
using OpenQA.Selenium.BiDi.Modules.BrowsingContext;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Remote;

namespace OpenQA.Selenium.BiDi
{
    [TestClass]
    public class LoggingTestBiDi
    {
        IWebDriver driver;

        BiDi bidi;

        BrowsingContext context;

        [TestInitialize]
        public async Task AutoStartDriver()
        {

            FirefoxOptions capability = new FirefoxOptions();

            var browserstackOptions = new Dictionary<string, object>
            {
                { "os", "OS X" },
                { "sessionName", "C# Selenium BiDi" },
                { "seleniumVersion", "4.24.0"},
                { "seleniumBidi", true }
            };

            capability.AddAdditionalOption("bstack:options", browserstackOptions);

            capability.UseWebSocketUrl = true;

           // driver = new FirefoxDriver(capability);
            driver = new RemoteWebDriver(new Uri("https://username:password@hub-cloud.browserstack.com/wd/hub"), capability);
            context = await driver.AsBiDiContextAsync();

            bidi = context.BiDi;

        }

        [TestMethod]
        public async Task ConsoleLogs()
        {
            TaskCompletionSource<Entry> tcs = new();

            await using var subscription = await context.Log.OnEntryAddedAsync(tcs.SetResult);

            driver.Navigate().GoToUrl("https://www.selenium.dev/selenium/web/bidi/logEntryAdded.html");
            driver.FindElement(By.Id("consoleLog")).Click();

            var logEntry = await tcs.Task.WaitAsync(TimeSpan.FromSeconds(5));

            Console.WriteLine(logEntry.Text);

        Assert.AreEqual(logEntry.Source.Context, context);
        Assert.AreEqual(logEntry.Text, "Hello, world!");
        Assert.AreEqual(logEntry.Level, Level.Info);
        }

        [TestCleanup]
        public async Task Cleanup()
        {
            if (bidi is not null)
            {
                await bidi.DisposeAsync();
            }

            driver?.Dispose();
        }
    }
}