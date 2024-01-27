while ($true) {
    $memoryUsage = Get-WmiObject Win32_OperatingSystem
    $freeMemoryMB = [math]::Round($memoryUsage.FreePhysicalMemory / 1MB, 2)
    $totalMemoryMB = [math]::Round($memoryUsage.TotalVisibleMemorySize / 1MB, 2)
    $memoryUsagePercent = [math]::Round(($freeMemoryMB / $totalMemoryMB) * 100, 2)

    $cpuUsage = Get-WmiObject Win32_Processor
    $cpuUsagePercent = [math]::Round($cpuUsage.LoadPercentage, 2)

    $diskUsage = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'"
    $freeSpaceGB = [math]::Round($diskUsage.FreeSpace / 1GB, 2)
    $totalSpaceGB = [math]::Round($diskUsage.Size / 1GB, 2)
    $usedSpaceGB = [math]::Round($totalSpaceGB - $freeSpaceGB, 2)
    $diskUsagePercent = [math]::Round(($usedSpaceGB / $totalSpaceGB) * 100, 2)

    $result = @{
        "MemoryUsagePercent" = $memoryUsagePercent
        "DiskUsagePercent" = $diskUsagePercent
        "CpuUsagePercent" = $cpuUsagePercent
    }

    # Convertir le résultat en JSON et l'afficher
  $result | ConvertTo-Json | Set-Content -Path "C:\Users\pc\Desktop\4 eme annee\Interconnection Reseaux\Monitoring\app\admin\templates\admin\systemInfo.json"


    # Attendre quelques secondes avant de recommencer
    Start-Sleep -Seconds 10
}

