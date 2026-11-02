param([switch]$Check)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$utf8 = [System.Text.UTF8Encoding]::new($false)
$pages = Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.html' |
    Where-Object { $_.FullName -notmatch '[\\/](\.git|\.mirror-cache|\.runtime|node_modules)[\\/]' }
$brandingSource = @'
using System;
using System.Text.RegularExpressions;

public static class HiTechBranding
{
    static readonly Regex Tokens = new Regex(@"<script\b[^>]*>.*?</script\s*>|<style\b[^>]*>.*?</style\s*>|<!--.*?-->|<[^>]+>|[^<]+", RegexOptions.IgnoreCase | RegexOptions.Singleline | RegexOptions.Compiled);
    static readonly Regex Brands = new Regex(@"Ascolite|Aswani|Aswini", RegexOptions.IgnoreCase | RegexOptions.Compiled);
    static readonly Regex Attributes = new Regex(@"\b(alt|title|content|aria-label)=""([^""]*)""", RegexOptions.IgnoreCase | RegexOptions.Compiled);

    static string Text(string value)
    {
        if (!Brands.IsMatch(value)) return value;
        value = Regex.Replace(value, @"(?i)\s*\(formerly known as\s+(?:Aswani|Aswini)\s+Construction\s+Pvt\.?\s*Ltd\.?\)", "");
        value = Regex.Replace(value, @"(?i)(?:Aswani|Aswini)\s+(?:Industries|Construction)\s+(?:(?:Pvt\.?|Private)\s*)?(?:Ltd\.?|Limited)?", "HI TECH");
        return Brands.Replace(value, "HI TECH");
    }

    static string Token(Match token)
    {
        string value = token.Value;
        if (Regex.IsMatch(value, @"(?is)^<script\b") && value.Contains("application/ld+json"))
            return Regex.Replace(value, @"""(?:\\.|[^""\\])*""", entry => entry.Value.Contains("http") ? entry.Value : Text(entry.Value));
        if (Regex.IsMatch(value, @"(?is)^<(?:script|style)\b|^<!--")) return value;
        if (!value.StartsWith("<")) return Text(value);
        if (Regex.IsMatch(value, @"(?i)^<link\b") && Regex.IsMatch(value, @"(?i)rel=""(?:shortcut )?icon"""))
        {
            value = Regex.Replace(value, @"(?i)\bhref=""[^""]*""", "href=\"images/svg/logo.svg?v=hi-tech\"");
            value = Regex.Replace(value, @"(?i)\btype=""[^""]*""", "type=\"image/svg+xml\"");
        }
        if (Regex.IsMatch(value, @"(?i)^<iframe\b") && value.Contains("google.com/maps"))
            value = Regex.Replace(value, @"(?i)\bsrc\s*=\s*""[^""]*""", "src=\"https://www.google.com/maps?q=Rola%2C%20Dungari%2C%20Valsad&amp;output=embed\"");
        if (Regex.IsMatch(value, @"(?i)^<img\b") && value.Contains("images/svg/logo.svg"))
        {
            value = Regex.Replace(value, @"(?i)\balt=""[^""]*""", "alt=\"HI TECH\"");
            value = Regex.Replace(value, @"(?i)\bsrc=""images/svg/logo\.svg(?:\?[^""]*)?""", "src=\"images/svg/logo.svg?v=hi-tech\"");
        }
        return Attributes.Replace(value, attribute => {
            string content = attribute.Groups[2].Value;
            if (content.Contains("http") || content.Contains("/index.html")) return attribute.Value;
            return attribute.Groups[1].Value + "=\"" + Text(content) + "\"";
        });
    }

    public static string Rewrite(string source)
    {
        source = Regex.Replace(source, @"(?is)(?:Aswani|Aswini)\s+Industries\s+Pvt\.?\s*Ltd\.?\s*150,\s*GIDC,\s*Pandesara Road,\s*Laxmi Narayan Nagar,\s*Pandesara GIDC,\s*Udhana,\s*Surat,\s*Gujarat\s*394221", "HI TECH<br>Rola, Dungari, Valsad");
        return Tokens.Replace(source, Token);
    }
}
'@
$typeName = 'HiTechBranding' + (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.Substring(0, 12)
if (-not ($typeName -as [type])) {
    Add-Type -TypeDefinition $brandingSource.Replace('HiTechBranding', $typeName)
}
$brandType = $typeName -as [type]

$changed = 0
foreach ($page in $pages) {
    $original = [System.IO.File]::ReadAllText($page.FullName)
    $updated = $brandType::Rewrite($original)
    if ($Check) {
        if ($updated -cne $original) { throw "Old branding remains in $($page.FullName)" }
    } elseif ($updated -cne $original) {
        [System.IO.File]::WriteAllText($page.FullName, $updated, $utf8)
        $changed++
    }
}
if ($Check) {
    $logo = [xml][System.IO.File]::ReadAllText((Join-Path $root 'images/svg/logo.svg'))
    if ($logo.svg.title.InnerText -ne 'HI TECH' -and $logo.svg.title -ne 'HI TECH') { throw 'Incorrect logo title' }
    Write-Output "PASS: $($pages.Count) HTML files checked for visible branding and metadata; logo SVG is valid."
} else {
    Copy-Item -LiteralPath (Join-Path $root 'images/svg/hi-tech-logo.svg') -Destination (Join-Path $root 'images/svg/logo.svg') -Force
    Write-Output "Updated $changed HTML files and replaced the shared logo.svg."
}