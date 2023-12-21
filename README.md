# Code Treemap Search Visualizer

When refactoring large code bases, it is easier for code reviews when we submit multiple pull requests. By visualizing it as a treemap, it would be easy to navigate different directories to figure out which ones we can combine in the same PR by looking at the # of files.

## How to use
Generate the treemap for all files that contain these keywords:
```
python treemap.py absl::optional absl::nullopt absl::make_optional third_party/abseil-cpp/absl/types/optional.h
```
Open up `index.html` or serve it:
```
python -m http.server
```

## Treemap example
![Screenshot](screenshot.png)
