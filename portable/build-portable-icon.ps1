param(
    [string]$InputPng = "assets/password_ninja.png",
    [string]$OutputIco = "assets/password_ninja_portable.ico"
)

$ErrorActionPreference = 'Stop'

$source = [System.Drawing.Image]::FromFile((Resolve-Path $InputPng))
try {
    $bitmap = New-Object System.Drawing.Bitmap 256, 256
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.Clear([System.Drawing.Color]::White)
        $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceOver
        $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

        $scale = [Math]::Min(220.0 / $source.Width, 220.0 / $source.Height)
        $drawWidth = [int]($source.Width * $scale)
        $drawHeight = [int]($source.Height * $scale)
        $x = [int]((256 - $drawWidth) / 2)
        $y = [int]((256 - $drawHeight) / 2 - 8)
        $graphics.DrawImage($source, $x, $y, $drawWidth, $drawHeight)

        $badgeBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(220, 124, 58, 237))
        $badgeRect = New-Object System.Drawing.Rectangle 150, 12, 94, 44
        $graphics.FillRectangle($badgeBrush, $badgeRect)

        $font = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
        $textBrush = [System.Drawing.Brushes]::White
        $textSize = $graphics.MeasureString("P", $font)
        $textX = 150 + [int](($badgeRect.Width - $textSize.Width) / 2)
        $textY = 12 + [int](($badgeRect.Height - $textSize.Height) / 2) - 1
        $graphics.DrawString("P", $font, $textBrush, $textX, $textY)

        New-Item -ItemType Directory -Force (Split-Path $OutputIco) | Out-Null
        $icon = [System.Drawing.Icon]::FromHandle($bitmap.GetHicon())
        try {
            $stream = [System.IO.File]::Open($OutputIco, [System.IO.FileMode]::Create)
            try {
                $icon.Save($stream)
            }
            finally {
                $stream.Dispose()
            }
        }
        finally {
            $icon.Dispose()
        }
    }
    finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}
finally {
    $source.Dispose()
}
