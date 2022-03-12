Run Gallery API Tests:
1. Install Java
2. Install Maven
3. Go to the directory with pom.xml file `<dir>\gallery-api\tests-gallery-api>`
4. run command: `mvn -Dtest=<Test class> test`

	* mvn -Dtest=GetCharactersTests test
	* mvn -Dtest=LikesTests test
	* mvn -Dtest=ViewsTests test
	* mvn -Dtest=ContactUsTests test
	* mvn -Dtest=AuthenticationTests test (not implemented yet)
