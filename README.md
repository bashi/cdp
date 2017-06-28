# cdp: Chrome Debugging Protocol

## Example usage

```
$ python -m scripts.cli  # Launches IPython shell
In [1]: page = devtools.CreateNewPage()
In [2]: actions.Navigate(page, 'http://www.example.com')
In [3]: page.Call('Page.reload', { 'ignoreCache': True })
```
