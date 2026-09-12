import asyncio

from course_knowledge.mcp_servers import create_author_server, create_student_server


def tool_names(server) -> set[str]:
    return {tool.name for tool in asyncio.run(server.list_tools())}


def test_author_and_student_servers_have_separate_least_privilege_tools() -> None:
    author_tools = tool_names(create_author_server())
    student_tools = tool_names(create_student_server())

    assert {"bestitcourses_list_courses", "bestitcourses_list_modules", "bestitcourses_get_module_assets", "bestitcourses_search_author_knowledge"} <= author_tools
    assert {"bestitcourses_student_courses", "bestitcourses_student_modules", "bestitcourses_student_search", "bestitcourses_student_ask"} <= student_tools
    assert "bestitcourses_get_module_assets" not in student_tools
    assert "bestitcourses_search_author_knowledge" not in student_tools
