---
title: "Converting raw Nikon NEF files to DNG and back on Linux"
description: "Converting raw Nikon NEF files to DNG and back on Linux"
date: 2021-02-05T09:33:00Z
draft: false
toc: false
slug: "converting_raw_nikon_nef_files_to_dng_and_back_on_linux"
categories:
  - photography
tags:
  - linux
  - raw
  - nef
  - dng
  - convert
---

Regardless of whether it makes sense or not to convert raw files to DNG, you
might choose a middleground solution and embed the original raw file in a DNG
file.  
The major drawback to this solution is that the resulting DNG file will
be roughly double in size when compared with the original raw file.  
The benefit of emdedding a raw files in a DNG file that you can easily extract
it later on.


## Step 1 - Install Adobe DNG Converter

You can find a very good tutorial on how to install it on Linux on 
RawTherapee's website: [https://rawpedia.rawtherapee.com/How_to_convert_raw_formats_to_DNG#Installing_Adobe_DNG_Converter_in_Linux](https://rawpedia.rawtherapee.com/How_to_convert_raw_formats_to_DNG#Installing_Adobe_DNG_Converter_in_Linux)

Once DNG Converter is installed, create a `dng` alias to start it from CLI:

```shell
alias dng='WINEPREFIX="$HOME/WinePrefixes/DNGConverter" wine "$HOME/WinePrefixes/DNGConverter/drive_c/Program Files/Adobe/Adobe DNG Converter/Adobe DNG Converter.exe"'
```


## Step 2 - Convert NEF files to DNG

`cd` to a directory with your `NEF` files and simply execute:

```shell
dng ./
```

It will bring the DNG Converter window up:
{{< gallery >}}
{{< figure link="/img/2021/02/05/01-dng_converter.png" thumb="-thumb" size="604x660" caption="Adobe DNG Converter main window" >}}
{{< /gallery >}}


Click `Change Preferences` and check `Embed Origianal Raw File`:
{{< gallery >}}
{{< figure link="/img/2021/02/05/02-dng_converter_preferences.png" thumb="-thumb" size="598x697" caption="Adobe DNG Converter preferences window" >}}
{{< /gallery >}}

Lastly, hit `Convert` button and wait for the conversion to finish:
03-dng_converter_conversion_status.png
{{< gallery >}}
{{< figure link="/img/2021/02/05/03-dng_converter_conversion_status.png" thumb="-thumb" size="548x401" caption="Adobe DNG Converter conversion status window" >}}
{{< /gallery >}}


## Step 3 - Extract embeded RAW NEF file from DNG

To extract an emdedded RAW NEF file from a DNG file, we'll use the amazing [ExifTool](https://exiftool.org) by Phil Harvey.

```shell
exiftool -b -originalrawimage DSC_0001-original.dng > DSC_0001-extracted.nef
```

## Step 4 - Compare extracted file with the original

To ensure that both files are identicall, run a simple diff:

```shell
$ diff --report-identical-files DSC_0001-original.nef DSC_0001-extracted.nef
Files DSC_0001-original.nef and DSC_0001-extracted.nef are identical
```

