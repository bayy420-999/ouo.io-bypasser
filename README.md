# ouo.io Link Bypasser

## Quick Start

### Usage

* Import module
  ```python
  import asyncio # You need asyncio for running main() function
  from ouo import OuoBypasser
  ```

* Use context manager
  ```python
  
  async def main():
      # Storing single url
      url = 'https://ouo.io/XGts9gT'
      
      # Storing multiple url with iterable (list, set, tuple)
      urls = ['https://ouo.io/XGts9gT', 'https://ouo.io/gGhs9hT']

      async with OuoBypasser() as bp:
          # Adding single url
          await bp.add_task(url)

          # Or you can add multiple url too
          for url in urls:
              await bp.add_task(url)

          # Then call the run() method
          await bp.run()

          # Get the results
          print(bp.results)
          # bp.results returning list that contains Result object
          # Result object contains original_link and bypassed_link

          # Accessing result
          res = bp.results
          print(res[0].bypassed_link)

  # Run main() function
  if __name__ == '__main__':
      asyncio.run(main())
  ```

* You can also use the low level API
  ```python
  async def main():
      url = 'https://ouo.io/XGts9gT'
      bp = OuoBypasser()
      await bp.bypass(url)
      print(bp.results)

      # Just don't forget to close connection if you didn't use context manager
      await bp.session.close()

  # Run main() function
  if __name__ == '__main__':
      asyncio.run(main())
  ```
