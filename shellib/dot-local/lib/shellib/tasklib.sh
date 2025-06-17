#!/usr/bin/env bash

# Task library - provides help functionality for task files

# List all functions defined in the current environment
list_functions() {
    declare -F | awk '{print $3}'
}

# Extract usage information from a function
get_function_usage() {
    local func_name="$1"
    local file="${2:-$0}"
    
    # Get the function definition and extract Usage: comments
    awk -v func="$func_name" '
    /^[[:space:]]*'"$func_name"'[[:space:]]*\(\)/ {
        in_func = 1
        next
    }
    in_func && /^[[:space:]]*}[[:space:]]*$/ {
        in_func = 0
    }
    in_func && /^[[:space:]]*#[[:space:]]*Usage:/ {
        sub(/^[[:space:]]*#[[:space:]]*/, "", $0)
        print $0
    }
    ' "$file"
}

# Display help for all functions in a task file
show_task_help() {
    local file="${1:-$0}"
    local func_list=$(list_functions | sort)
    
    echo "Available tasks:"
    echo "================"
    echo
    
    for func in $func_list; do
        # Skip internal functions and the help function itself
        if [[ ! "$func" =~ ^(_|show_task_help|list_functions|get_function_usage) ]]; then
            local usage=$(get_function_usage "$func" "$file")
            if [[ -n "$usage" ]]; then
                printf "%-30s %s\n" "$func" "- $usage"
            else
                printf "%-30s\n" "$func"
            fi
        fi
    done
    echo
    echo "Run any task by calling it directly: ./tasks <task_name>"
}

# Alternative: Show detailed help for a specific function
show_function_help() {
    local func_name="$1"
    local file="${2:-$0}"
    
    if ! declare -f "$func_name" >/dev/null 2>&1; then
        echo "Error: Function '$func_name' not found" >&2
        return 1
    fi
    
    echo "Help for: $func_name"
    echo "==================="
    
    local usage=$(get_function_usage "$func_name" "$file")
    if [[ -n "$usage" ]]; then
        echo "$usage"
    else
        echo "No usage information available"
    fi
}